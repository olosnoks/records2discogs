#!/usr/bin/env python3
"""
Batch Cleanup Script for records2discogs
Backs up CSVs, appends to master, cleans up vinyl-record-indexing
"""

import os
import csv
import shutil
from datetime import datetime
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent
VINYL_INDEXING_DIR = ROOT_DIR / "vinyl-record-indexing"
OUTPUT_CSV = VINYL_INDEXING_DIR / "output.csv"
VINYLS_DIR = VINYL_INDEXING_DIR / "vinyls"
BACKUP_DIR = ROOT_DIR / "csv-backups"
MASTER_CSV = ROOT_DIR / "master.csv"

def ensure_directories():
    """Create necessary directories if they don't exist"""
    BACKUP_DIR.mkdir(exist_ok=True)
    print(f"✓ Backup directory ready")

def backup_batch_csv():
    """Backup the output CSV with timestamp to csv-backups/"""
    if not OUTPUT_CSV.exists():
        print(f"⚠ No output CSV found at {OUTPUT_CSV}")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"batch_{timestamp}.csv"
    backup_path = BACKUP_DIR / backup_filename
    
    shutil.copy2(OUTPUT_CSV, backup_path)
    print(f"✓ Backed up CSV to: {backup_path}")
    return backup_path

def append_to_master(source_csv):
    """Append batch CSV to master.csv in root"""
    if not source_csv or not source_csv.exists():
        print("⚠ No source CSV to append")
        return
    
    # Read the batch CSV
    with open(source_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        print("⚠ Batch CSV is empty")
        return
    
    # Check if master exists
    master_exists = MASTER_CSV.exists()
    
    # Write to master
    with open(MASTER_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        if not master_exists:
            # Write header if new file
            writer.writerow(rows[0])
            writer.writerows(rows[1:])
            print(f"✓ Created master.csv with {len(rows)-1} records")
        else:
            # Append data (skip header)
            writer.writerows(rows[1:])
            print(f"✓ Appended {len(rows)-1} records to master.csv")

def delete_output_csv():
    """Delete the output CSV from vinyl-record-indexing after backup"""
    if OUTPUT_CSV.exists():
        OUTPUT_CSV.unlink()
        print(f"✓ Deleted output.csv from vinyl-record-indexing")
    else:
        print(f"⚠ Output CSV not found: {OUTPUT_CSV}")

def delete_vinyls_folder():
    """Delete the vinyls image folder from vinyl-record-indexing"""
    if VINYLS_DIR.exists():
        shutil.rmtree(VINYLS_DIR)
        print(f"✓ Deleted vinyls folder from vinyl-record-indexing")
    else:
        print(f"⚠ Vinyls folder not found: {VINYLS_DIR}")

def get_master_stats():
    """Get statistics about the master CSV"""
    if not MASTER_CSV.exists():
        return 0
    
    with open(MASTER_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        row_count = sum(1 for row in reader) - 1  # Subtract header
    return row_count

def main():
    print("\n" + "="*60)
    print("RECORDS2DISCOGS - Batch Cleanup")
    print("="*60 + "\n")
    
    # Step 1: Create directories
    ensure_directories()
    
    # Step 2: Backup the output CSV to csv-backups/
    print("\n[1/4] Backing up batch CSV...")
    backup_path = backup_batch_csv()
    
    # Step 3: Append to master.csv in root
    print("\n[2/4] Appending to master.csv...")
    append_to_master(backup_path)
    
    # Step 4: Delete output.csv from vinyl-record-indexing
    print("\n[3/4] Deleting output.csv from vinyl-record-indexing...")
    delete_output_csv()
    
    # Step 5: Delete vinyls folder from vinyl-record-indexing
    print("\n[4/4] Deleting vinyls folder from vinyl-record-indexing...")
    delete_vinyls_folder()
    
    # Summary
    print("\n" + "="*60)
    print("CLEANUP COMPLETE")
    print("="*60)
    total_records = get_master_stats()
    print(f"✓ Total records in master.csv: {total_records}")
    print(f"✓ Timestamped backup: {backup_path}")
    print(f"✓ Master CSV: {MASTER_CSV}")
    print(f"✓ vinyl-record-indexing cleaned and ready for next run")
    print("\nReady for next batch!\n")

if __name__ == "__main__":
    main()
