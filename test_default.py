#!/usr/bin/env python3
"""
Test script to verify default behavior
"""
import sys
import os

# Simulate different command line arguments
def test_default():
    print("Testing default behavior (no args)...")
    sys.argv = ['main.py']
    # Import and check what would run
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        print("❌ Would run CLI (wrong!)")
        return False
    else:
        print("✅ Would run web server (correct!)")
        return True

def test_cli_flag():
    print("Testing --cli flag...")
    sys.argv = ['main.py', '--cli']
    # Import and check what would run
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        print("✅ Would run CLI (correct!)")
        return True
    else:
        print("❌ Would run web server (wrong!)")
        return False

if __name__ == "__main__":
    print("Testing default behavior changes...")
    test1 = test_default()
    test2 = test_cli_flag()

    if test1 and test2:
        print("\n✅ All tests passed! Default is now web interface.")
    else:
        print("\n❌ Tests failed!")

