# Scripts Directory

This directory contains automation scripts and data files for the New-Grad-Positions repository.

## Files

### listings.json
**Comprehensive job listings database** containing all unique job postings from the entire repository history.

- **Total Listings**: 4,188 unique job postings
- **Date Range**: July 19, 2023 - September 30, 2025
- **Companies**: 1,335 unique companies
- **Size**: 2.33 MB

This file is automatically updated and contains both active and historical job listings. See [LISTINGS_HISTORY.md](LISTINGS_HISTORY.md) for detailed statistics.

### LISTINGS_HISTORY.md
Documentation and statistics about the comprehensive listings.json file, including methodology, top companies, and historical insights.

### build_comprehensive_listings.py
Python script to regenerate the comprehensive listings.json file from the complete git history.

**Usage:**
```bash
python3 build_comprehensive_listings.py
```

This script:
1. Fetches all commits that modified listings.json
2. Extracts job listings from each commit
3. Deduplicates by job ID
4. Sorts by date posted
5. Outputs comprehensive listings.json

**Note**: Processing all commits takes approximately 5-10 minutes.

### contribution_approved.py
Script for processing and approving job listing contributions.

### update_readmes.py
Script to update README files with current job listings.

### util.py
Utility functions used by other scripts in this directory.

## Updating the Comprehensive Listings

The comprehensive listings.json file can be regenerated at any time by running:

```bash
cd .github/scripts
python3 build_comprehensive_listings.py
```

This will process the entire git history and create a file containing all unique job listings that have ever appeared in the repository.
