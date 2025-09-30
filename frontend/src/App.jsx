import { useState } from 'react';
import { hashLocalImage, searchProxy, compareThumbnails } from './api';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [hashResult, setHashResult] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  const [compareResults, setCompareResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showTakedownModal, setShowTakedownModal] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setHashResult(null);
      setSearchResults(null);
      setCompareResults(null);
      setError(null);
    }
  };

  const handleComputeHash = async () => {
    if (!selectedFile) {
      setError('Please select an image file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await hashLocalImage(selectedFile);
      setHashResult(result);
    } catch (err) {
      setError(`Error computing hash: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRunSearch = async () => {
    if (!hashResult) {
      setError('Please compute hash first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Step 1: Get candidate URLs (mock)
      const searchRes = await searchProxy(hashResult.phash);
      setSearchResults(searchRes);

      // Step 2: Compare thumbnails
      const candidateUrls = searchRes.candidates.map(c => c.url);
      const compareRes = await compareThumbnails(hashResult.phash, candidateUrls);
      setCompareResults(compareRes);
    } catch (err) {
      setError(`Error during search: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateTakedown = (result) => {
    setSelectedMatch(result);
    setShowTakedownModal(true);
  };

  const handleDownloadReport = () => {
    if (!compareResults) return;

    const matches = compareResults.results.filter(r => r.is_match);
    const report = {
      timestamp: new Date().toISOString(),
      demo_mode: true,
      local_hash: hashResult?.phash,
      matches: matches.map(m => ({
        url: m.url,
        similarity: m.similarity,
        phash: m.phash,
      })),
      safety_notice: 'This is a DEMO report with MOCK data.',
    };

    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `consent-guardian-report-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-red-600 text-white py-6 shadow-lg">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold">Consent Guardian POC</h1>
          <p className="text-red-100 mt-2">
            ⚠️ DEMONSTRATION ONLY - Not for production use
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Safety Notice */}
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">Safety Notice</h3>
              <div className="mt-2 text-sm text-yellow-700">
                <ul className="list-disc pl-5 space-y-1">
                  <li>This is a proof-of-concept demonstration only</li>
                  <li>Uses MOCK search results - real APIs are disabled</li>
                  <li>All processing happens locally - no images are stored</li>
                  <li>If you encounter illegal content, contact authorities immediately</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Step 1: Upload Image */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Step 1: Upload Consenting Image</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select image file (consenting photos only)
              </label>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-md file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
              />
            </div>
            {selectedFile && (
              <div className="text-sm text-gray-600">
                Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
              </div>
            )}
            <button
              onClick={handleComputeHash}
              disabled={!selectedFile || loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              Compute Hash
            </button>
          </div>
        </div>

        {/* Hash Result */}
        {hashResult && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Hash Result</h2>
            <div className="space-y-2">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">Format:</span> {hashResult.metadata.format}
                </div>
                <div>
                  <span className="font-medium">Size:</span> {hashResult.metadata.size[0]}x{hashResult.metadata.size[1]}
                </div>
              </div>
              <div className="mt-4">
                <span className="font-medium">Perceptual Hash:</span>
                <div className="mt-1 p-3 bg-gray-100 rounded font-mono text-sm break-all">
                  {hashResult.phash}
                </div>
              </div>
              <div className="mt-4">
                <button
                  onClick={handleRunSearch}
                  disabled={loading}
                  className="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 disabled:bg-gray-400"
                >
                  Run Safe Search (Demo)
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Search Results */}
        {searchResults && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Search Results</h2>
            {searchResults.is_mock && (
              <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-4 text-sm text-blue-800">
                ℹ️ {searchResults.message}
              </div>
            )}
            <div className="text-sm text-gray-600 mb-2">
              Found {searchResults.candidates.length} candidate(s)
            </div>
          </div>
        )}

        {/* Comparison Results */}
        {compareResults && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Comparison Results</h2>
            <div className="text-sm text-gray-600 mb-4">
              Threshold for match: {(compareResults.threshold * 100).toFixed(0)}%
            </div>
            
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      URL
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Similarity
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Match
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Action
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {compareResults.results.map((result, idx) => (
                    <tr key={idx} className={result.is_match ? 'bg-red-50' : ''}>
                      <td className="px-6 py-4 text-sm text-gray-900 break-all max-w-xs">
                        {result.url}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        <div className="flex items-center">
                          <div className="w-16">
                            {(result.similarity * 100).toFixed(1)}%
                          </div>
                          <div className="w-32 bg-gray-200 rounded-full h-2 ml-2">
                            <div
                              className={`h-2 rounded-full ${
                                result.is_match ? 'bg-red-600' : 'bg-blue-600'
                              }`}
                              style={{ width: `${result.similarity * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {result.is_match ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                            MATCH
                          </span>
                        ) : (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                            No match
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {result.is_match && (
                          <button
                            onClick={() => handleGenerateTakedown(result)}
                            className="text-blue-600 hover:text-blue-900"
                          >
                            Generate Takedown
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-4">
              <button
                onClick={handleDownloadReport}
                className="bg-purple-600 text-white px-6 py-2 rounded-md hover:bg-purple-700"
              >
                Download Report (Metadata Only)
              </button>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-gray-600">Processing...</p>
          </div>
        )}
      </main>

      {/* Takedown Modal */}
      {showTakedownModal && selectedMatch && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={() => setShowTakedownModal(false)}></div>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                  Takedown Request Template
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">URL</label>
                    <div className="mt-1 p-2 bg-gray-100 rounded text-sm break-all">
                      {selectedMatch.url}
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Similarity Score</label>
                    <div className="mt-1 p-2 bg-gray-100 rounded text-sm">
                      {(selectedMatch.similarity * 100).toFixed(1)}%
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Suggested Message</label>
                    <textarea
                      readOnly
                      rows="6"
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 text-sm"
                      value={`I have found a potentially non-consensual image at the following URL:

${selectedMatch.url}

The image appears to match my photo with ${(selectedMatch.similarity * 100).toFixed(0)}% similarity based on perceptual hashing analysis.

I did not provide consent for this image to be published or distributed.

I request immediate removal of this content and confirmation of removal.

Thank you.`}
                    />
                  </div>
                  
                  <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
                    <p className="text-sm text-yellow-800 font-medium mb-2">⚠️ IMPORTANT:</p>
                    <ul className="text-xs text-yellow-700 space-y-1 list-disc pl-5">
                      <li>Do NOT attach images to takedown requests</li>
                      <li>If content appears illegal, contact authorities immediately:</li>
                      <li>NCMEC CyberTipline: <a href="https://www.cybertipline.org" className="underline" target="_blank" rel="noopener noreferrer">cybertipline.org</a></li>
                      <li>INHOPE hotlines: <a href="https://www.inhope.org" className="underline" target="_blank" rel="noopener noreferrer">inhope.org</a></li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  onClick={() => {
                    const template = `I have found a potentially non-consensual image at: ${selectedMatch.url}\n\nSimilarity: ${(selectedMatch.similarity * 100).toFixed(0)}%\n\nI did not provide consent for this image to be published.\n\nPlease remove it immediately.`;
                    navigator.clipboard.writeText(template);
                    alert('Template copied to clipboard');
                  }}
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Copy to Clipboard
                </button>
                <button
                  type="button"
                  onClick={() => setShowTakedownModal(false)}
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center text-sm">
          <p>Consent Guardian POC - Educational Demo Only</p>
          <p className="mt-2 text-gray-400">
            Not for production use. See SAFETY_AND_LEGAL.md for important information.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
