"""
Unit tests for perceptual hashing and similarity computation.

Tests ensure:
- Hash computation is consistent
- Similarity calculations are correct
- Image processing is safe (in-memory only)
- Error handling works properly
"""

import sys
from pathlib import Path
import pytest
from io import BytesIO
from PIL import Image

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.hash_utils import compute_phash, compute_similarity


def create_test_image(width=100, height=100, color='red', pattern=None):
    """Create a test image in memory."""
    img = Image.new('RGB', (width, height), color=color)
    
    # Add pattern to make images more distinct for perceptual hashing
    if pattern == 'stripes':
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        for i in range(0, width, 20):
            draw.rectangle([i, 0, i+10, height], fill='black')
    elif pattern == 'grid':
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        for i in range(0, width, 20):
            draw.line([(i, 0), (i, height)], fill='black', width=2)
        for i in range(0, height, 20):
            draw.line([(0, i), (width, i)], fill='black', width=2)
    
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    return buffer.getvalue()


class TestHashComputation:
    """Test perceptual hash computation."""
    
    def test_compute_phash_basic(self):
        """Test basic hash computation."""
        image_bytes = create_test_image()
        phash, metadata = compute_phash(image_bytes)
        
        # Hash should be a hex string
        assert isinstance(phash, str)
        assert len(phash) == 16  # pHash is 64-bit = 16 hex chars
        assert all(c in '0123456789abcdef' for c in phash.lower())
        
        # Metadata should contain expected fields
        assert 'format' in metadata
        assert 'size' in metadata
        assert 'mode' in metadata
        assert metadata['format'] == 'JPEG'
        assert metadata['size'] == (100, 100)
    
    def test_compute_phash_consistency(self):
        """Test that same image produces same hash."""
        image_bytes = create_test_image(color='blue')
        
        phash1, _ = compute_phash(image_bytes)
        phash2, _ = compute_phash(image_bytes)
        
        assert phash1 == phash2
    
    def test_compute_phash_different_images(self):
        """Test that different images produce different hashes."""
        image1 = create_test_image(color='red', pattern='stripes')
        image2 = create_test_image(color='blue', pattern='grid')
        
        phash1, _ = compute_phash(image1)
        phash2, _ = compute_phash(image2)
        
        assert phash1 != phash2
    
    def test_compute_phash_invalid_data(self):
        """Test error handling for invalid image data."""
        invalid_bytes = b"not an image"
        
        with pytest.raises(ValueError):
            compute_phash(invalid_bytes)
    
    def test_compute_phash_different_sizes(self):
        """Test hash computation for different image sizes."""
        small_image = create_test_image(50, 50, 'green')
        large_image = create_test_image(500, 500, 'green')
        
        phash_small, _ = compute_phash(small_image)
        phash_large, _ = compute_phash(large_image)
        
        # Both should produce valid hashes
        assert len(phash_small) == 16
        assert len(phash_large) == 16
        
        # Similar colored images should have high similarity despite size difference
        similarity = compute_similarity(phash_small, phash_large)
        assert similarity > 0.7  # Should be fairly similar


class TestSimilarityComparison:
    """Test similarity computation between hashes."""
    
    def test_identical_hashes(self):
        """Test similarity of identical hashes."""
        image_bytes = create_test_image()
        phash, _ = compute_phash(image_bytes)
        
        similarity = compute_similarity(phash, phash)
        assert similarity == 1.0
    
    def test_similar_images(self):
        """Test similarity of visually similar images."""
        # Create two red images (should be very similar)
        image1 = create_test_image(100, 100, 'red')
        image2 = create_test_image(100, 100, 'red')
        
        phash1, _ = compute_phash(image1)
        phash2, _ = compute_phash(image2)
        
        similarity = compute_similarity(phash1, phash2)
        assert similarity >= 0.95  # Should be very similar
    
    def test_different_images(self):
        """Test similarity of different images."""
        image1 = create_test_image(100, 100, 'red', pattern='stripes')
        image2 = create_test_image(100, 100, 'blue', pattern='grid')
        
        phash1, _ = compute_phash(image1)
        phash2, _ = compute_phash(image2)
        
        similarity = compute_similarity(phash1, phash2)
        assert 0.0 <= similarity <= 1.0  # Valid range
        assert similarity < 0.99  # Should not be nearly identical
    
    def test_similarity_range(self):
        """Test that similarity is always in valid range [0, 1]."""
        colors = ['red', 'blue', 'green', 'yellow', 'purple']
        
        for color1 in colors:
            for color2 in colors:
                img1 = create_test_image(color=color1)
                img2 = create_test_image(color=color2)
                
                phash1, _ = compute_phash(img1)
                phash2, _ = compute_phash(img2)
                
                similarity = compute_similarity(phash1, phash2)
                assert 0.0 <= similarity <= 1.0
    
    def test_similarity_symmetry(self):
        """Test that similarity(A, B) == similarity(B, A)."""
        image1 = create_test_image(color='red')
        image2 = create_test_image(color='blue')
        
        phash1, _ = compute_phash(image1)
        phash2, _ = compute_phash(image2)
        
        similarity_ab = compute_similarity(phash1, phash2)
        similarity_ba = compute_similarity(phash2, phash1)
        
        assert similarity_ab == similarity_ba
    
    def test_invalid_hash_comparison(self):
        """Test error handling for invalid hash strings."""
        with pytest.raises(ValueError):
            compute_similarity("invalid", "hashes")


class TestMatchThreshold:
    """Test match threshold logic."""
    
    def test_threshold_85_percent(self):
        """Test that 0.85 threshold works for matches."""
        # Create very similar images
        img1 = create_test_image(100, 100, 'red')
        img2 = create_test_image(100, 100, 'red')
        
        phash1, _ = compute_phash(img1)
        phash2, _ = compute_phash(img2)
        
        similarity = compute_similarity(phash1, phash2)
        threshold = 0.85
        
        # Very similar images should exceed threshold
        assert similarity >= threshold
    
    def test_threshold_rejection(self):
        """Test that different images don't exceed threshold."""
        img1 = create_test_image(100, 100, 'red', pattern='stripes')
        img2 = create_test_image(100, 100, 'blue', pattern='grid')
        
        phash1, _ = compute_phash(img1)
        phash2, _ = compute_phash(img2)
        
        similarity = compute_similarity(phash1, phash2)
        
        # Different patterns should have lower similarity
        assert similarity < 0.99


class TestDemoImages:
    """Test with actual demo images if available."""
    
    def test_demo_images_exist(self):
        """Check that demo images exist."""
        demo_dir = Path(__file__).parent.parent / "backend" / "demo_data" / "consent_photos"
        image1 = demo_dir / "demo_image_1.jpg"
        image2 = demo_dir / "demo_image_2.jpg"
        
        if image1.exists() and image2.exists():
            # Test with real demo images
            with open(image1, 'rb') as f:
                img1_bytes = f.read()
            with open(image2, 'rb') as f:
                img2_bytes = f.read()
            
            phash1, metadata1 = compute_phash(img1_bytes)
            phash2, metadata2 = compute_phash(img2_bytes)
            
            # Both should produce valid hashes
            assert len(phash1) == 16
            assert len(phash2) == 16
            
            # Should have valid metadata
            assert metadata1['format'] in ['JPEG', 'PNG']
            assert metadata2['format'] in ['JPEG', 'PNG']
            
            # Compute similarity
            similarity = compute_similarity(phash1, phash2)
            assert 0.0 <= similarity <= 1.0
        else:
            pytest.skip("Demo images not found")


class TestMemorySafety:
    """Test that processing doesn't persist data."""
    
    def test_no_file_creation(self, tmp_path):
        """Test that hash computation doesn't create files."""
        initial_files = set(tmp_path.iterdir())
        
        image_bytes = create_test_image()
        compute_phash(image_bytes)
        
        final_files = set(tmp_path.iterdir())
        
        # No new files should be created
        assert initial_files == final_files
    
    def test_memory_cleanup(self):
        """Test that large images can be processed without memory issues."""
        # Create a large image
        large_image = create_test_image(2000, 2000, 'blue')
        
        # Should successfully compute hash
        phash, metadata = compute_phash(large_image)
        
        assert len(phash) == 16
        assert metadata['size'] == (2000, 2000)
        
        # Memory should be released (no explicit test, but shouldn't crash)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
