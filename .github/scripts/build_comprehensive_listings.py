#!/usr/bin/env python3
"""
Complete script to build a comprehensive listings.json file by extracting ALL unique job listings
from the ENTIRE git history. This will take time but ensures completeness.
"""

import json
import subprocess
import sys
from datetime import datetime
import os

def get_all_commits_for_file(repo_path, file_path, branch='upstream/dev'):
    """Get all commit hashes that modified the listings.json file."""
    cmd = ['git', '-C', repo_path, 'log', '--reverse', '--pretty=format:%H', branch, '--', file_path]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    commits = [c for c in result.stdout.strip().split('\n') if c]
    return commits

def extract_all_listings_comprehensive(repo_path, file_path, branch='upstream/dev'):
    """Extract ALL job listings from ALL commits - the complete approach."""
    
    print("Fetching complete commit history...")
    commits = get_all_commits_for_file(repo_path, file_path, branch)
    total_commits = len(commits)
    print(f"Found {total_commits} commits to process")
    
    # Use a dictionary keyed by job ID
    all_listings = {}
    
    # Process commits in batches using git archive or git show
    print("\nProcessing commits (this will take a while for completeness)...")
    
    for idx, commit_hash in enumerate(commits):
        if (idx + 1) % 100 == 0:
            print(f"Progress: {idx + 1}/{total_commits} commits ({(idx+1)*100//total_commits}%)")
        
        # Use git show to get file content at this commit
        cmd = ['git', '-C', repo_path, 'show', f'{commit_hash}:{file_path}']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            continue
        
        try:
            listings = json.loads(result.stdout)
            if not isinstance(listings, list):
                continue
            
            for listing in listings:
                if not isinstance(listing, dict) or 'id' not in listing:
                    continue
                
                job_id = listing['id']
                
                # Keep the most recent version based on date_updated
                if job_id not in all_listings:
                    all_listings[job_id] = listing
                else:
                    current_date = all_listings[job_id].get('date_updated', 0)
                    new_date = listing.get('date_updated', 0)
                    if new_date > current_date:
                        all_listings[job_id] = listing
                        
        except json.JSONDecodeError:
            continue
    
    print(f"\nCompleted! Extracted {len(all_listings)} unique job listings from {total_commits} commits")
    
    # Convert to list and sort by date_posted (newest first)
    result = list(all_listings.values())
    result.sort(key=lambda x: x.get('date_posted', 0), reverse=True)
    
    return result

def main():
    repo_path = '/home/runner/work/New-Grad-Positions/New-Grad-Positions'
    file_path = '.github/scripts/listings.json'
    output_path = '/home/runner/work/New-Grad-Positions/New-Grad-Positions/.github/scripts/listings.json'
    
    print("=" * 80)
    print("Building COMPLETE listings.json from ENTIRE git history")
    print("This will process ALL commits to ensure nothing is missed")
    print("=" * 80)
    print()
    
    comprehensive_listings = extract_all_listings_comprehensive(
        repo_path, file_path, branch='upstream/dev'
    )
    
    # Statistics
    print("\n" + "=" * 80)
    print("FINAL STATISTICS:")
    print("=" * 80)
    print(f"Total unique job listings: {len(comprehensive_listings)}")
    print(f"Active listings: {sum(1 for l in comprehensive_listings if l.get('active', False))}")
    print(f"Inactive listings: {sum(1 for l in comprehensive_listings if not l.get('active', False))}")
    
    # Date range
    if comprehensive_listings:
        dates = [l.get('date_posted', 0) for l in comprehensive_listings if l.get('date_posted')]
        if dates:
            earliest = min(dates)
            latest = max(dates)
            print(f"\nDate range: {datetime.fromtimestamp(earliest).strftime('%Y-%m-%d')} to {datetime.fromtimestamp(latest).strftime('%Y-%m-%d')}")
    
    # Company statistics
    companies = {}
    for listing in comprehensive_listings:
        company = listing.get('company_name', 'Unknown')
        companies[company] = companies.get(company, 0) + 1
    
    print(f"\nUnique companies: {len(companies)}")
    print("\nTop 10 companies by number of listings:")
    top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
    for company, count in top_companies:
        print(f"  {company}: {count} listings")
    
    # Write the comprehensive file
    print(f"\nWriting comprehensive listings to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(comprehensive_listings, f, indent=4, ensure_ascii=False)
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
    print(f"\nFile written successfully!")
    print(f"File size: {file_size:.2f} MB")
    print(f"Total listings: {len(comprehensive_listings)}")
    print("\n" + "=" * 80)
    print("COMPLETE! You now have ALL job listings from the entire history.")
    print("=" * 80)

if __name__ == '__main__':
    main()
