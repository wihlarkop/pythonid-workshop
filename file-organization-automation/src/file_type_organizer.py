"""
File Type Organizer - Automatically sort files by type into folders
Organizes files based on their extensions into categorized folders
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class FileTypeOrganizer:
    """Organizes files by type into categorized folders"""

    def __init__(self, source_dir: str, output_dir: str = None):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir) if output_dir else self.source_dir / "organized"

        # File type categories
        self.file_categories = {
            'Documents': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
                'description': 'Text documents and PDFs'
            },
            'Spreadsheets': {
                'extensions': ['.xlsx', '.xls', '.csv', '.ods', '.numbers'],
                'description': 'Excel and other spreadsheet files'
            },
            'Presentations': {
                'extensions': ['.pptx', '.ppt', '.odp', '.key'],
                'description': 'PowerPoint and other presentation files'
            },
            'Images': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
                'description': 'Photos and image files'
            },
            'Videos': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
                'description': 'Video and movie files'
            },
            'Audio': {
                'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
                'description': 'Music and audio files'
            },
            'Archives': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.tar.gz'],
                'description': 'Compressed and archive files'
            },
            'Code': {
                'extensions': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go'],
                'description': 'Source code and scripts'
            },
            'Executables': {
                'extensions': ['.exe', '.msi', '.deb', '.dmg', '.app'],
                'description': 'Applications and installers'
            },
            'Other': {
                'extensions': [],  # Catch-all for unknown extensions
                'description': 'Files with unrecognized extensions'
            }
        }

        self.moved_files = []
        self.stats = {
            'total_files': 0,
            'moved_files': 0,
            'skipped_files': 0,
            'categories_used': set()
        }

    def get_file_category(self, file_path: Path) -> str:
        """Determine the category for a file based on its extension"""
        extension = file_path.suffix.lower()

        for category, info in self.file_categories.items():
            if extension in info['extensions']:
                return category

        return 'Other'

    def create_category_folders(self):
        """Create folders for each file category"""
        print("Creating category folders...")

        for category in self.file_categories.keys():
            category_path = self.output_dir / category
            category_path.mkdir(parents=True, exist_ok=True)

        print(f"Category folders created in: {self.output_dir}")

    def organize_files(self, move_files: bool = True):
        """Organize files by type into category folders"""
        print(f"\nStarting file organization...")
        print(f"Source directory: {self.source_dir}")
        print(f"Output directory: {self.output_dir}")
        print(f"Operation: {'MOVE' if move_files else 'COPY'} files")

        # Create category folders
        self.create_category_folders()

        # Get all files in source directory
        files = [f for f in self.source_dir.iterdir() if f.is_file()]
        self.stats['total_files'] = len(files)

        print(f"\nProcessing {len(files)} files...")

        for file_path in files:
            try:
                # Determine category
                category = self.get_file_category(file_path)
                self.stats['categories_used'].add(category)

                # Create destination path
                dest_folder = self.output_dir / category
                dest_path = dest_folder / file_path.name

                # Handle filename conflicts
                counter = 1
                original_dest = dest_path
                while dest_path.exists():
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_path = dest_folder / f"{stem}_{counter}{suffix}"
                    counter += 1

                # Move or copy the file
                if move_files:
                    shutil.move(str(file_path), str(dest_path))
                    operation = "moved"
                else:
                    shutil.copy2(str(file_path), str(dest_path))
                    operation = "copied"

                # Record the operation
                self.moved_files.append({
                    'original_path': file_path,
                    'new_path': dest_path,
                    'category': category,
                    'operation': operation
                })

                self.stats['moved_files'] += 1
                try:
                    print(f"  {operation.capitalize()}: {file_path.name} -> {category}/{dest_path.name}")
                except UnicodeEncodeError:
                    print(f"  {operation.capitalize()}: [Unicode filename] -> {category}/[Unicode filename]")

            except Exception as e:
                try:
                    print(f"  Error processing {file_path.name}: {e}")
                except UnicodeEncodeError:
                    print(f"  Error processing [Unicode filename]: {e}")
                self.stats['skipped_files'] += 1

    def generate_report(self) -> str:
        """Generate a summary report of the organization process"""
        report = []
        report.append("FILE ORGANIZATION REPORT")
        report.append("=" * 50)
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Source Directory: {self.source_dir}")
        report.append(f"Output Directory: {self.output_dir}")
        report.append("")

        # Summary statistics
        report.append("SUMMARY:")
        report.append(f"  Total files processed: {self.stats['total_files']}")
        report.append(f"  Files successfully organized: {self.stats['moved_files']}")
        report.append(f"  Files skipped (errors): {self.stats['skipped_files']}")
        report.append(f"  Categories used: {len(self.stats['categories_used'])}")
        report.append("")

        # Category breakdown
        category_counts = {}
        for file_info in self.moved_files:
            category = file_info['category']
            category_counts[category] = category_counts.get(category, 0) + 1

        report.append("CATEGORY BREAKDOWN:")
        for category, count in sorted(category_counts.items()):
            description = self.file_categories[category]['description']
            percentage = (count / self.stats['moved_files'] * 100) if self.stats['moved_files'] > 0 else 0
            report.append(f"  {category:15s}: {count:3d} files ({percentage:5.1f}%) - {description}")

        report.append("")

        # Detailed file list
        report.append("DETAILED FILE LIST:")
        for category in sorted(self.stats['categories_used']):
            category_files = [f for f in self.moved_files if f['category'] == category]
            if category_files:
                report.append(f"\n{category}:")
                for file_info in category_files:
                    report.append(f"  {file_info['original_path'].name} -> {file_info['new_path'].name}")

        return "\n".join(report)

    def save_report(self, report_path: str = None):
        """Save the organization report to a file"""
        if not report_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.output_dir.parent / f"organization_report_{timestamp}.txt"

        report_content = self.generate_report()

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"\nReport saved: {report_path}")
        return report_path

    def print_summary(self):
        """Print a summary of the organization process"""
        print("\n" + "=" * 60)
        print("FILE ORGANIZATION COMPLETED!")
        print("=" * 60)

        print(f"Files processed: {self.stats['total_files']}")
        print(f"Files organized: {self.stats['moved_files']}")
        print(f"Files skipped: {self.stats['skipped_files']}")
        print(f"Categories used: {len(self.stats['categories_used'])}")

        if self.stats['categories_used']:
            print(f"\nCategories created:")
            for category in sorted(self.stats['categories_used']):
                count = len([f for f in self.moved_files if f['category'] == category])
                print(f"  {category}: {count} files")

        print(f"\nOrganized files location: {self.output_dir}")

    def run_organization(self, move_files: bool = True, save_report: bool = True):
        """Run the complete file organization process"""
        print("STARTING FILE TYPE ORGANIZATION")
        print("=" * 60)

        # Organize files
        self.organize_files(move_files)

        # Print summary
        self.print_summary()

        # Save report
        if save_report:
            self.save_report()


def main():
    """Main function to demonstrate file organization"""
    # Use sample_files as source
    source_path = Path(__file__).parent.parent / 'sample_files'

    if not source_path.exists() or not any(source_path.iterdir()):
        print("Error: No sample files found!")
        print("Please run create_sample_files.py first to generate test files.")
        return

    # Create organizer
    organizer = FileTypeOrganizer(
        source_dir=str(source_path),
        output_dir=str(source_path.parent / 'output' / 'organized_files')
    )

    # Run organization (copy files to preserve originals for testing)
    organizer.run_organization(move_files=False, save_report=True)


if __name__ == "__main__":
    main()