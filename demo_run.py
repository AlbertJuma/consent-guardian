#!/usr/bin/env python3
"""
Consent Guardian - Safe Local Demo Script

This script demonstrates the core functionality of the Consent Guardian POC
using safe, synthetic test images. All operations are performed locally with
logging to stdout only - NO file writes except logs.

SAFETY: This script uses ONLY consenting demo images from demo_data/consent_photos/
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.hash_utils import compute_phash, compute_similarity


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_info(label, value):
    """Print formatted info line."""
    print(f"  {label:<30} {value}")


def run_demo():
    """Run the complete demo workflow."""
    
    print_header("CONSENT GUARDIAN - SAFE LOCAL DEMO")
    print("\n  ⚠️  DEMO MODE - Using synthetic test images only")
    print("  ⚠️  No real photos, no scraping, no external APIs")
    print("  ⚠️  All processing in memory - no file persistence\n")
    
    # Demo data paths
    demo_dir = Path(__file__).parent / "backend" / "demo_data" / "consent_photos"
    image1_path = demo_dir / "demo_image_1.jpg"
    image2_path = demo_dir / "demo_image_2.jpg"
    
    if not image1_path.exists() or not image2_path.exists():
        print("❌ Error: Demo images not found!")
        print(f"   Expected: {demo_dir}")
        return 1
    
    # Step 1: Compute hash for first image
    print_header("STEP 1: Compute Perceptual Hash (pHash)")
    
    with open(image1_path, 'rb') as f:
        image1_bytes = f.read()
    
    phash1, metadata1 = compute_phash(image1_bytes)
    
    print_info("Image:", image1_path.name)
    print_info("Format:", metadata1['format'])
    print_info("Size:", f"{metadata1['size'][0]}x{metadata1['size'][1]}")
    print_info("Mode:", metadata1['mode'])
    print_info("Computed pHash:", phash1)
    print(f"\n  ✓ Hash computed successfully (in memory only)")
    
    # Step 2: Compute hash for second image
    print_header("STEP 2: Compute Hash for Comparison Image")
    
    with open(image2_path, 'rb') as f:
        image2_bytes = f.read()
    
    phash2, metadata2 = compute_phash(image2_bytes)
    
    print_info("Image:", image2_path.name)
    print_info("Format:", metadata2['format'])
    print_info("Size:", f"{metadata2['size'][0]}x{metadata2['size'][1]}")
    print_info("Computed pHash:", phash2)
    
    # Step 3: Compare hashes
    print_header("STEP 3: Compare Perceptual Hashes")
    
    similarity = compute_similarity(phash1, phash2)
    threshold = 0.85
    
    print_info("Hash 1:", phash1)
    print_info("Hash 2:", phash2)
    print_info("Similarity Score:", f"{similarity:.3f} ({similarity*100:.1f}%)")
    print_info("Match Threshold:", f"{threshold:.2f} ({threshold*100:.0f}%)")
    print_info("Is Match?", "YES ✓" if similarity >= threshold else "NO ✗")
    
    # Step 4: Simulate search results (MOCK)
    print_header("STEP 4: Simulate Reverse Image Search (MOCK)")
    
    mock_candidates = [
        {"url": "https://example.com/demo-thumbnail-1.jpg", "source": "mock_search"},
        {"url": "https://example.com/demo-thumbnail-2.jpg", "source": "mock_search"},
        {"url": "https://example.com/demo-thumbnail-3.jpg", "source": "mock_search"},
    ]
    
    print("\n  🔍 Mock search results (external APIs disabled):")
    for i, candidate in enumerate(mock_candidates, 1):
        print(f"     {i}. {candidate['url']}")
        print(f"        Source: {candidate['source']}")
    
    print("\n  ℹ️  Real reverse-image search requires:")
    print("     - Legal review and approval")
    print("     - Partnership agreements with API providers")
    print("     - Configuration: allow_external_fetch=true")
    
    # Step 5: Simulate comparison results
    print_header("STEP 5: Simulate Thumbnail Comparison (DEMO)")
    
    print("\n  📊 Simulated similarity scores:")
    simulated_results = [
        {"url": mock_candidates[0]["url"], "similarity": 0.92, "is_match": True},
        {"url": mock_candidates[1]["url"], "similarity": 0.45, "is_match": False},
        {"url": mock_candidates[2]["url"], "similarity": 0.88, "is_match": True},
    ]
    
    for result in simulated_results:
        match_icon = "🔴 MATCH" if result["is_match"] else "⚪ No match"
        print(f"     {match_icon} - {result['similarity']:.2f} - {result['url']}")
    
    # Step 6: Generate takedown template
    print_header("STEP 6: Takedown Template Generation")
    
    matches = [r for r in simulated_results if r["is_match"]]
    
    if matches:
        print(f"\n  Found {len(matches)} potential match(es) above threshold\n")
        
        for i, match in enumerate(matches, 1):
            print(f"  --- Template for Match {i} ---")
            print(f"  URL: {match['url']}")
            print(f"  Similarity: {match['similarity']:.2f}")
            print(f"  Timestamp: {datetime.utcnow().isoformat()}")
            print(f"\n  Suggested message:")
            print(f"  \"I have found a potentially non-consensual image at the URL above.")
            print(f"   The image appears to match my photo with {match['similarity']*100:.0f}% similarity.")
            print(f"   I did not provide consent for this image to be published.")
            print(f"   Please remove it immediately and confirm removal.\"")
            print()
        
        print("  ⚠️  IMPORTANT:")
        print("     - Do NOT attach images to takedown requests")
        print("     - If content appears illegal, contact authorities immediately:")
        print("       • NCMEC CyberTipline: https://www.cybertipline.org")
        print("       • INHOPE hotlines: https://www.inhope.org")
    
    # Step 7: Export report (metadata only)
    print_header("STEP 7: Export Metadata Report")
    
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "demo_mode": True,
        "original_image": {
            "phash": phash1,
            "metadata": metadata1
        },
        "matches": matches,
        "safety_notice": "This is a DEMO report with MOCK data. No real images were processed."
    }
    
    report_json = json.dumps(report, indent=2)
    print(f"\n  Report (JSON):\n")
    print("  " + report_json.replace("\n", "\n  "))
    
    print("\n  ✓ Report generated (stdout only - no file written)")
    
    # Summary
    print_header("DEMO COMPLETE")
    
    print("\n  Summary:")
    print(f"     ✓ Computed pHash for {len([phash1, phash2])} images")
    print(f"     ✓ Performed similarity comparison")
    print(f"     ✓ Simulated reverse-image search (mock)")
    print(f"     ✓ Generated takedown templates for {len(matches)} match(es)")
    print(f"     ✓ All processing in memory - no persistence")
    
    print("\n  Next Steps:")
    print("     1. Review docs/SAFETY_AND_LEGAL.md")
    print("     2. Run backend: cd backend && uvicorn app.main:app --reload")
    print("     3. Run frontend: cd frontend && npm start")
    print("     4. Access UI at http://localhost:3000")
    
    print("\n" + "=" * 80 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(run_demo())
