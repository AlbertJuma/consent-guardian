/**
 * API client for Consent Guardian backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Compute perceptual hash for uploaded image
 */
export async function hashLocalImage(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/hash-local`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to compute hash');
  }

  return response.json();
}

/**
 * Proxy reverse image search (returns mock results by default)
 */
export async function searchProxy(phash) {
  const response = await fetch(`${API_BASE_URL}/search-proxy`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ phash }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Search failed');
  }

  return response.json();
}

/**
 * Compare local hash against candidate URLs
 */
export async function compareThumbnails(localPhash, candidateUrls) {
  const response = await fetch(`${API_BASE_URL}/compare`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      local_phash: localPhash,
      candidate_urls: candidateUrls,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Comparison failed');
  }

  return response.json();
}
