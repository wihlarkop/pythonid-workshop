"""
Duplicate File Detector - Find and manage duplicate files
Uses file content hashing to identify exact duplicates
"""

import hashlib
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import send2trash


class DuplicateFileDetector:
    """Detects and manages duplicate files based on content"""

    def __init__(self, search_dir: str, output_dir: str = None):
        self.search_dir = Path(search_dir)
        self.output_dir = Path(output_dir) if output_dir else self.search_dir.parent / "output"
        self.output_dir.mkdir(exist_ok=True)

        self.file_hashes = defaultdict(list)
        self.duplicates = {}
        self.stats = {
            'total_files': 0,
            'unique_files': 0,
            'duplicate_groups': 0,
            'total_duplicates': 0,
            'space_wasted': 0,
            'files_deleted': 0,
            'space_recovered': 0
        }

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (OSError, PermissionError) as e:
            print(f"  Warning: Cannot read {file_path.name}: {e}")
            return None

    def scan_for_duplicates(self, include_subdirs: bool = True):
        """Scan directory for duplicate files"""
        print(f"Scanning for duplicates in: {self.search_dir}")
        print(f"Include subdirectories: {include_subdirs}")

        # Get all files
        if include_subdirs:
            files = [f for f in self.search_dir.rglob('*') if f.is_file()]
        else:
            files = [f for f in self.search_dir.iterdir() if f.is_file()]

        self.stats['total_files'] = len(files)
        print(f"Found {len(files)} files to analyze...")

        # Calculate hash for each file
        for i, file_path in enumerate(files, 1):
            if i % 10 == 0 or i == len(files):
                print(f"  Processing file {i}/{len(files)}...")

            file_hash = self.calculate_file_hash(file_path)
            if file_hash:
                file_info = {
                    'path': file_path,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                }
                self.file_hashes[file_hash].append(file_info)

        # Identify duplicates (groups with more than one file)
        self.duplicates = {
            hash_val: files
            for hash_val, files in self.file_hashes.items()
            if len(files) > 1
        }

        # Update statistics
        self.stats['unique_files'] = len(self.file_hashes)
        self.stats['duplicate_groups'] = len(self.duplicates)
        self.stats['total_duplicates'] = sum(len(files) - 1 for files in self.duplicates.values())

        # Calculate wasted space (size of all duplicates except one original per group)
        for files in self.duplicates.values():
            file_size = files[0]['size']  # All files in group have same size
            duplicate_count = len(files) - 1  # Exclude one original
            self.stats['space_wasted'] += file_size * duplicate_count

        print(f"Scan completed!")

    def get_duplicate_summary(self) -> Dict:
        """Get summary of duplicate analysis"""
        return {
            'total_files': self.stats['total_files'],
            'unique_files': self.stats['unique_files'],
            'duplicate_groups': self.stats['duplicate_groups'],
            'total_duplicates': self.stats['total_duplicates'],
            'space_wasted_bytes': self.stats['space_wasted'],
            'space_wasted_mb': self.stats['space_wasted'] / (1024 * 1024),
            'largest_duplicate_group': max(len(files) for files in self.duplicates.values()) if self.duplicates else 0
        }

    def print_duplicate_report(self):
        """Print detailed duplicate file report"""
        print("\n" + "=" * 70)
        print("DUPLICATE FILE ANALYSIS REPORT")
        print("=" * 70)

        summary = self.get_duplicate_summary()

        print(f"\nSUMMARY:")
        print(f"  Total files scanned: {summary['total_files']:,}")
        print(f"  Unique files: {summary['unique_files']:,}")
        print(f"  Duplicate groups found: {summary['duplicate_groups']:,}")
        print(f"  Total duplicate files: {summary['total_duplicates']:,}")
        print(f"  Wasted storage space: {summary['space_wasted_mb']:.2f} MB")
        print(f"  Largest duplicate group: {summary['largest_duplicate_group']} files")

        if not self.duplicates:
            print("\nNo duplicate files found!")
            return

        print(f"\nDETAILED DUPLICATE GROUPS:")
        print("-" * 70)

        for i, (file_hash, files) in enumerate(self.duplicates.items(), 1):
            file_size = files[0]['size']
            duplicate_count = len(files) - 1
            wasted_space = file_size * duplicate_count

            print(f"\nGroup {i}: {len(files)} identical files")
            print(f"  File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
            print(f"  Wasted space: {wasted_space:,} bytes ({wasted_space / 1024:.1f} KB)")
            print(f"  Hash: {file_hash}")
            print(f"  Files:")

            # Sort by modification date (oldest first)
            sorted_files = sorted(files, key=lambda x: x['modified'])

            for j, file_info in enumerate(sorted_files):
                marker = "[ORIGINAL]" if j == 0 else "[DUPLICATE]"
                try:
                    print(f"    {marker} {file_info['path'].name}")
                    print(f"              Path: {file_info['path']}")
                    print(f"              Modified: {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
                except UnicodeEncodeError:
                    print(f"    {marker} [Unicode filename]")
                    print(f"              Path: [Unicode path]")
                    print(f"              Modified: {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}")

    def delete_duplicates(self, keep_oldest: bool = True, use_trash: bool = True):
        """Delete duplicate files, keeping one copy"""
        if not self.duplicates:
            print("No duplicates to delete!")
            return

        print(f"\nStarting duplicate file deletion...")
        print(f"Keep policy: {'Oldest file' if keep_oldest else 'Newest file'}")
        print(f"Delete method: {'Move to trash' if use_trash else 'Permanent deletion'}")

        deleted_files = []
        total_space_recovered = 0

        for file_hash, files in self.duplicates.items():
            # Sort files by modification date
            sorted_files = sorted(files, key=lambda x: x['modified'])

            # Choose which file to keep
            if keep_oldest:
                keep_file = sorted_files[0]
                delete_files = sorted_files[1:]
            else:
                keep_file = sorted_files[-1]
                delete_files = sorted_files[:-1]

            print(f"\nProcessing group with {len(files)} files:")
            try:
                print(f"  Keeping: {keep_file['path'].name}")
            except UnicodeEncodeError:
                print(f"  Keeping: [Unicode filename]")

            # Delete duplicate files
            for file_info in delete_files:
                try:
                    file_path = file_info['path']
                    file_size = file_info['size']

                    if use_trash:
                        send2trash.send2trash(str(file_path))
                        action = "moved to trash"
                    else:
                        file_path.unlink()
                        action = "deleted permanently"

                    deleted_files.append(file_info)
                    total_space_recovered += file_size
                    self.stats['files_deleted'] += 1

                    try:
                        print(f"    Deleted: {file_path.name} ({action})")
                    except UnicodeEncodeError:
                        print(f"    Deleted: [Unicode filename] ({action})")

                except Exception as e:
                    try:
                        print(f"    Error deleting {file_path.name}: {e}")
                    except UnicodeEncodeError:
                        print(f"    Error deleting [Unicode filename]: {e}")

        self.stats['space_recovered'] = total_space_recovered

        print(f"\n" + "=" * 50)
        print("DUPLICATE DELETION COMPLETED!")
        print("=" * 50)
        print(f"Files deleted: {self.stats['files_deleted']}")
        print(f"Space recovered: {total_space_recovered / (1024 * 1024):.2f} MB")

        return deleted_files

    def export_duplicate_report(self, report_path: str = None):
        """Export duplicate analysis to text file"""
        if not report_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.output_dir / f"duplicate_report_{timestamp}.txt"

        report = []
        report.append("DUPLICATE FILE ANALYSIS REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Search Directory: {self.search_dir}")
        report.append("")

        # Summary
        summary = self.get_duplicate_summary()
        report.append("SUMMARY:")
        report.append(f"  Total files scanned: {summary['total_files']:,}")
        report.append(f"  Unique files: {summary['unique_files']:,}")
        report.append(f"  Duplicate groups: {summary['duplicate_groups']:,}")
        report.append(f"  Total duplicates: {summary['total_duplicates']:,}")
        report.append(f"  Wasted space: {summary['space_wasted_mb']:.2f} MB")
        report.append("")

        # Detailed groups
        if self.duplicates:
            report.append("DUPLICATE GROUPS:")
            report.append("-" * 30)

            for i, (file_hash, files) in enumerate(self.duplicates.items(), 1):
                file_size = files[0]['size']
                wasted_space = file_size * (len(files) - 1)

                report.append(f"\nGroup {i}: {len(files)} files")
                report.append(f"  Size: {file_size:,} bytes")
                report.append(f"  Wasted: {wasted_space:,} bytes")
                report.append(f"  Hash: {file_hash}")

                sorted_files = sorted(files, key=lambda x: x['modified'])
                for j, file_info in enumerate(sorted_files):
                    marker = "[KEEP]" if j == 0 else "[DELETE]"
                    report.append(f"    {marker} {file_info['path']}")
                    report.append(f"         Modified: {file_info['modified']}")
        else:
            report.append("No duplicates found.")

        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"Report exported: {report_path}")
        return report_path

    def run_duplicate_detection(self, include_subdirs: bool = True,
                              delete_duplicates: bool = False,
                              keep_oldest: bool = True):
        """Run complete duplicate detection process"""
        print("STARTING DUPLICATE FILE DETECTION")
        print("=" * 60)

        # Scan for duplicates
        self.scan_for_duplicates(include_subdirs)

        # Print report
        self.print_duplicate_report()

        # Export report
        self.export_duplicate_report()

        # Delete duplicates if requested
        if delete_duplicates and self.duplicates:
            print("\nDo you want to delete the duplicate files? (y/N): ", end="")
            response = input().strip().lower()
            if response == 'y':
                self.delete_duplicates(keep_oldest=keep_oldest, use_trash=True)
            else:
                print("Deletion cancelled. Duplicates preserved.")


def main():
    """Main function to demonstrate duplicate detection"""
    # Use sample_files as source
    search_path = Path(__file__).parent.parent / 'sample_files'

    if not search_path.exists() or not any(search_path.iterdir()):
        print("Error: No sample files found!")
        print("Please run create_sample_files.py first to generate test files.")
        return

    # Create detector
    detector = DuplicateFileDetector(
        search_dir=str(search_path),
        output_dir=str(search_path.parent / 'output')
    )

    # Run detection (without automatic deletion for safety)
    detector.run_duplicate_detection(
        include_subdirs=False,
        delete_duplicates=False,  # Set to True to enable deletion prompt
        keep_oldest=True
    )


if __name__ == "__main__":
    main()