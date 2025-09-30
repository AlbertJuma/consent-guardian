#!/usr/bin/env python3
"""
Safety verification script for Consent Guardian POC.

This script verifies that all safety constraints are properly configured.
"""

import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} NOT FOUND: {filepath}")
        return False

def check_file_content(filepath, pattern, description):
    """Check if a file contains a specific pattern."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if pattern in content:
                print(f"✓ {description}")
                return True
            else:
                print(f"✗ {description} MISSING")
                return False
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        return False

def main():
    """Run all safety checks."""
    print("=" * 80)
    print("CONSENT GUARDIAN - SAFETY VERIFICATION")
    print("=" * 80)
    print()
    
    all_checks_passed = True
    
    # Check essential files exist
    print("Checking essential files...")
    all_checks_passed &= check_file_exists("README.md", "README")
    all_checks_passed &= check_file_exists("LICENSE", "LICENSE")
    all_checks_passed &= check_file_exists("docs/SAFETY_AND_LEGAL.md", "Safety documentation")
    all_checks_passed &= check_file_exists(".gitignore", ".gitignore")
    all_checks_passed &= check_file_exists("backend/app/config.example.yaml", "Config example")
    print()
    
    # Check safety defaults in config
    print("Checking safety defaults in config...")
    all_checks_passed &= check_file_content(
        "backend/app/config.example.yaml",
        "allow_external_fetch: false",
        "allow_external_fetch defaults to false"
    )
    all_checks_passed &= check_file_content(
        "backend/app/config.example.yaml",
        "escalate_to_hotline: false",
        "escalate_to_hotline defaults to false"
    )
    print()
    
    # Check gitignore excludes sensitive files
    print("Checking .gitignore excludes sensitive files...")
    all_checks_passed &= check_file_content(
        ".gitignore",
        "config.yaml",
        ".gitignore excludes config.yaml"
    )
    all_checks_passed &= check_file_content(
        ".gitignore",
        "node_modules/",
        ".gitignore excludes node_modules/"
    )
    all_checks_passed &= check_file_content(
        ".gitignore",
        ".env",
        ".gitignore excludes .env"
    )
    print()
    
    # Check README has legal disclaimer
    print("Checking README has legal disclaimer...")
    all_checks_passed &= check_file_content(
        "README.md",
        "CRITICAL SAFETY NOTICE",
        "README has critical safety notice"
    )
    all_checks_passed &= check_file_content(
        "README.md",
        "One-Paragraph Legal Disclaimer",
        "README has legal disclaimer section"
    )
    all_checks_passed &= check_file_content(
        "README.md",
        "CSAM",
        "README mentions CSAM reporting requirements"
    )
    print()
    
    # Check backend has safety constraints
    print("Checking backend safety constraints...")
    all_checks_passed &= check_file_content(
        "backend/app/main.py",
        "IMPORTANT SAFETY CONSTRAINTS",
        "Backend has safety notice"
    )
    all_checks_passed &= check_file_content(
        "backend/app/main.py",
        "NO image persistence",
        "Backend documents no persistence"
    )
    all_checks_passed &= check_file_content(
        "backend/app/hash_utils.py",
        "BytesIO",
        "Hash utils uses BytesIO for in-memory processing"
    )
    print()
    
    # Check LICENSE has disclaimers
    print("Checking LICENSE has proper disclaimers...")
    all_checks_passed &= check_file_content(
        "LICENSE",
        "IMPORTANT LEGAL NOTICE",
        "LICENSE has legal notice"
    )
    all_checks_passed &= check_file_content(
        "LICENSE",
        "CSAM",
        "LICENSE mentions CSAM"
    )
    all_checks_passed &= check_file_content(
        "LICENSE",
        "DEMONSTRATION ONLY",
        "LICENSE states demonstration only"
    )
    print()
    
    # Summary
    print("=" * 80)
    if all_checks_passed:
        print("✓ ALL SAFETY CHECKS PASSED")
        print()
        print("The Consent Guardian POC appears to be properly configured with")
        print("all required safety constraints and legal disclaimers.")
        return 0
    else:
        print("✗ SOME SAFETY CHECKS FAILED")
        print()
        print("Please review the failed checks above and ensure all safety")
        print("constraints are properly configured before using this software.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
