# Python File Integrity Monitor (FIM)

A lightweight security tool to monitor file system integrity using SHA-256 hashing.

## Features
- **Baseline Generation**: Snapshots a directory's "clean" state.
- **Real-time Detection**: Identifies file modifications, deletions, and new creations.
- **Memory Efficient**: Uses chunked hashing for large files.

## How to Run
1. `python fim.py --baseline`
2. `python fim.py --monitor`

## Why it's Secure
This tool follows the **Integrity** pillar of the CIA Triad by ensuring that any unauthorized change to sensitive system files is flagged immediately.
