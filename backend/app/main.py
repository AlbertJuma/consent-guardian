"""
FastAPI backend for Consent Guardian POC.

IMPORTANT SAFETY CONSTRAINTS:
- NO image persistence to disk
- NO scraping functionality
- Mock search by default
- Strict fetch limits for thumbnails
- Metadata logging only
"""

import io
import logging
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yaml

from app.hash_utils import compute_phash, compute_similarity, fetch_and_hash_thumbnail

# Configure logging (safe metadata only)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Consent Guardian API",
    description="POC API for non-consensual image detection (DEMO ONLY)",
    version="1.0.0"
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
try:
    with open("app/config.example.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    logger.warning("Config file not found, using defaults")
    config = {
        "allow_external_fetch": False,
        "similarity_threshold": 0.85,
        "fetch_limits": {"max_thumbnail_bytes": 262144, "timeout_seconds": 10}
    }


# Pydantic models
class HashResponse(BaseModel):
    phash: str
    metadata: dict
    timestamp: str


class SearchRequest(BaseModel):
    phash: Optional[str] = None
    image_url: Optional[str] = None


class CandidateURL(BaseModel):
    url: str
    source: str


class SearchResponse(BaseModel):
    candidates: List[CandidateURL]
    is_mock: bool
    message: str


class CompareRequest(BaseModel):
    local_phash: str
    candidate_urls: List[str]


class SimilarityResult(BaseModel):
    url: str
    similarity: float
    phash: str
    is_match: bool


class CompareResponse(BaseModel):
    results: List[SimilarityResult]
    threshold: float
    timestamp: str


@app.get("/")
async def root():
    """Health check and API info."""
    return {
        "status": "operational",
        "name": "Consent Guardian POC API",
        "version": "1.0.0",
        "warning": "DEMO ONLY - NOT FOR PRODUCTION USE",
        "safety_notice": "This API does not persist images or scrape websites"
    }


@app.post("/hash-local", response_model=HashResponse)
async def hash_local_image(file: UploadFile = File(...)):
    """
    Compute perceptual hash of uploaded image.
    
    SAFETY: Image is processed in memory only and NOT saved to disk.
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Validate size (prevent huge uploads)
        max_upload_size = 10 * 1024 * 1024  # 10 MB
        if len(contents) > max_upload_size:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        # Compute hash in memory
        phash, metadata = compute_phash(contents)
        
        # Log safe metadata only
        logger.info(f"Computed hash for image - format: {metadata.get('format')}, size: {metadata.get('size')}")
        
        # Immediately release memory
        del contents
        
        return HashResponse(
            phash=phash,
            metadata=metadata,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process image")


@app.post("/search-proxy", response_model=SearchResponse)
async def search_proxy(request: SearchRequest):
    """
    Reverse image search proxy endpoint.
    
    SAFETY: Returns MOCK results by default. 
    Real API integration requires legal review and config.allow_external_fetch=true
    
    TODO: Integrate with TinEye/Bing/Google APIs after:
    1. Legal review completed
    2. Partnership agreements signed
    3. API keys obtained
    4. Rate limiting configured
    """
    
    # EXPLICIT MOCK RESPONSE - DO NOT ENABLE WITHOUT LEGAL REVIEW
    if not config.get("allow_external_fetch", False):
        logger.info("Search request received - returning MOCK results (allow_external_fetch=false)")
        
        mock_candidates = [
            CandidateURL(
                url="https://example.com/demo-thumbnail-1.jpg",
                source="mock_search"
            ),
            CandidateURL(
                url="https://example.com/demo-thumbnail-2.jpg", 
                source="mock_search"
            ),
            CandidateURL(
                url="https://example.com/demo-thumbnail-3.jpg",
                source="mock_search"
            )
        ]
        
        return SearchResponse(
            candidates=mock_candidates,
            is_mock=True,
            message="MOCK results only - Real search disabled for safety. Enable in config after legal review."
        )
    
    # TODO: Real API integration code here
    # Example structure for TinEye:
    # if 'tineye' in config.get('api_keys', {}):
    #     api_key = config['api_keys']['tineye']
    #     # Make API call with proper error handling
    #     # Parse response and extract thumbnail URLs
    #     # Return real candidates
    
    raise HTTPException(
        status_code=501,
        detail="Real search API not implemented - requires legal review and partnership"
    )


@app.post("/compare", response_model=CompareResponse)
async def compare_thumbnails(request: CompareRequest):
    """
    Compare local hash against candidate thumbnail URLs.
    
    SAFETY CONSTRAINTS:
    - Only fetches small thumbnails (max 256 KB)
    - Does NOT save images to disk
    - Processes in memory only
    - Strict timeouts and limits
    """
    
    if not config.get("allow_external_fetch", False):
        # For demo mode, simulate comparisons without fetching
        logger.info(f"Compare request (DEMO mode) - local_hash: {request.local_phash[:16]}...")
        
        results = []
        for url in request.candidate_urls[:5]:  # Limit to 5 for demo
            # Simulate varying similarity scores for demo
            import hashlib
            simulated_score = (int(hashlib.md5(url.encode()).hexdigest(), 16) % 100) / 100.0
            
            results.append(SimilarityResult(
                url=url,
                similarity=simulated_score,
                phash="0" * 16,  # Mock hash
                is_match=simulated_score >= config.get("similarity_threshold", 0.85)
            ))
        
        return CompareResponse(
            results=results,
            threshold=config.get("similarity_threshold", 0.85),
            timestamp=datetime.utcnow().isoformat()
        )
    
    # Real comparison (when enabled)
    results = []
    max_bytes = config.get("fetch_limits", {}).get("max_thumbnail_bytes", 262144)
    timeout = config.get("fetch_limits", {}).get("timeout_seconds", 10)
    
    for url in request.candidate_urls[:20]:  # Max 20 candidates
        logger.info(f"Fetching thumbnail: {url}")
        
        thumbnail_hash, success = fetch_and_hash_thumbnail(url, max_bytes, timeout)
        
        if success:
            similarity = compute_similarity(request.local_phash, thumbnail_hash)
            is_match = similarity >= config.get("similarity_threshold", 0.85)
            
            results.append(SimilarityResult(
                url=url,
                similarity=round(similarity, 3),
                phash=thumbnail_hash,
                is_match=is_match
            ))
            
            logger.info(f"Comparison result - URL: {url}, similarity: {similarity:.3f}")
        else:
            logger.warning(f"Failed to fetch thumbnail: {url}")
    
    return CompareResponse(
        results=results,
        threshold=config.get("similarity_threshold", 0.85),
        timestamp=datetime.utcnow().isoformat()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
