"""
Perceptual hashing utilities for image comparison.

This module provides safe, in-memory image hashing functionality.
NO images are persisted to disk.
"""

import io
from typing import Tuple
import imagehash
from PIL import Image


def compute_phash(image_bytes: bytes) -> Tuple[str, dict]:
    """
    Compute perceptual hash (pHash) from image bytes.
    
    Args:
        image_bytes: Raw image data in bytes
        
    Returns:
        Tuple of (hash_string, metadata_dict)
        
    Raises:
        ValueError: If image cannot be processed
    """
    try:
        # Process in memory only - do NOT save to disk
        image_stream = io.BytesIO(image_bytes)
        img = Image.open(image_stream)
        
        # Extract safe metadata only
        metadata = {
            "format": img.format,
            "size": img.size,
            "mode": img.mode,
        }
        
        # Compute perceptual hash
        phash = imagehash.phash(img)
        hash_string = str(phash)
        
        # Immediately release resources
        img.close()
        image_stream.close()
        
        return hash_string, metadata
        
    except Exception as e:
        raise ValueError(f"Failed to process image: {str(e)}")


def compute_similarity(hash1: str, hash2: str) -> float:
    """
    Calculate similarity between two perceptual hashes.
    
    Args:
        hash1: First hash as string
        hash2: Second hash as string
        
    Returns:
        Similarity score between 0.0 (different) and 1.0 (identical)
    """
    try:
        h1 = imagehash.hex_to_hash(hash1)
        h2 = imagehash.hex_to_hash(hash2)
        
        # Hamming distance between hashes
        distance = h1 - h2
        
        # Convert to similarity score (0-1 range)
        # pHash produces 64-bit hash, max distance is 64
        max_distance = 64
        similarity = 1.0 - (distance / max_distance)
        
        return max(0.0, min(1.0, similarity))
        
    except Exception as e:
        raise ValueError(f"Failed to compare hashes: {str(e)}")


def fetch_and_hash_thumbnail(url: str, max_bytes: int = 262144, timeout: int = 10) -> Tuple[str, bool]:
    """
    Fetch a thumbnail image from URL and compute its hash.
    
    SAFETY CONSTRAINTS:
    - Only fetches small thumbnails (max 256 KB by default)
    - Does NOT save to disk
    - Strict timeout
    - User-agent identifies this project
    
    Args:
        url: URL of thumbnail to fetch
        max_bytes: Maximum bytes to download (default 256 KB)
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (hash_string, success_boolean)
    """
    import requests
    
    try:
        # Safety headers
        headers = {
            'User-Agent': 'ConsentGuardian-POC-Demo/1.0 (Educational; +https://github.com/AlbertJuma/consent-guardian)',
        }
        
        # Fetch with strict limits - do NOT follow redirects to other domains
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            stream=True,
            allow_redirects=False
        )
        
        if response.status_code != 200:
            return "", False
            
        # Read with size limit
        content = b""
        for chunk in response.iter_content(chunk_size=8192):
            content += chunk
            if len(content) > max_bytes:
                # Exceeded size limit - abort
                return "", False
                
        # Process in memory only
        hash_string, _ = compute_phash(content)
        
        # Ensure no persistence
        del content
        
        return hash_string, True
        
    except Exception:
        return "", False
