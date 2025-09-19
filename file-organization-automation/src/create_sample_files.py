"""
Create Sample Files for File Organization Automation Testing
Creates various file types with different naming patterns and dates
"""

import os
import random
from datetime import datetime, timedelta
from pathlib import Path


class SampleFileCreator:
    """Creates sample files for testing file organization automation"""

    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def create_sample_documents(self):
        """Create sample document files with various formats"""
        print("Creating sample documents...")

        documents = [
            # PDF files
            "Invoice_2024_001.pdf",
            "contract_client_abc.pdf",
            "report_quarterly_2024.pdf",
            "presentation_sales_deck.pdf",
            "manual_user_guide.pdf",

            # Word documents
            "proposal_project_alpha.docx",
            "minutes_meeting_20240315.docx",
            "template_letter_format.docx",
            "resume_john_doe.docx",

            # Excel files
            "budget_2024_annual.xlsx",
            "inventory_warehouse_data.xlsx",
            "sales_report_march.xlsx",
            "employee_list_2024.xlsx",

            # Text files
            "notes_daily_tasks.txt",
            "config_server_settings.txt",
            "log_system_errors.txt",
            "readme_project_info.txt"
        ]

        for doc in documents:
            file_path = self.base_path / doc
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Sample content for {doc}\nCreated on: {datetime.now()}\n")
                f.write("This is a test file for file organization automation.\n")

        print(f"Created {len(documents)} document files")

    def create_sample_images(self):
        """Create sample image files with various formats"""
        print("Creating sample images...")

        images = [
            # Photos with dates
            "IMG_20240315_143022.jpg",
            "photo_vacation_beach_2024.jpg",
            "screenshot_2024-03-15_154530.png",
            "profile_picture_john.jpg",
            "logo_company_final.png",

            # Graphics and designs
            "banner_website_header.jpg",
            "infographic_sales_data.png",
            "chart_performance_metrics.jpg",
            "diagram_network_architecture.png",
            "mockup_mobile_app.jpg"
        ]

        for img in images:
            file_path = self.base_path / img
            with open(file_path, 'wb') as f:
                # Create a minimal file (just header bytes for different formats)
                if img.endswith('.jpg') or img.endswith('.jpeg'):
                    f.write(b'\xff\xd8\xff\xe0')  # JPEG header
                elif img.endswith('.png'):
                    f.write(b'\x89PNG\r\n\x1a\n')  # PNG header
                f.write(f"Sample image data for {img}".encode())

        print(f"Created {len(images)} image files")

    def create_sample_media(self):
        """Create sample media files (video/audio)"""
        print("Creating sample media files...")

        media = [
            # Video files
            "presentation_demo_2024.mp4",
            "tutorial_how_to_setup.avi",
            "recording_meeting_march15.mov",
            "video_product_showcase.mkv",

            # Audio files
            "audio_interview_client.mp3",
            "music_background_corporate.wav",
            "podcast_episode_12.m4a",
            "voicemail_important_call.mp3"
        ]

        for media_file in media:
            file_path = self.base_path / media_file
            with open(file_path, 'wb') as f:
                # Create minimal headers for different media formats
                if media_file.endswith('.mp4'):
                    f.write(b'ftypisom')  # MP4 header
                elif media_file.endswith('.avi'):
                    f.write(b'RIFF....AVI ')  # AVI header
                elif media_file.endswith('.mp3'):
                    f.write(b'ID3')  # MP3 header
                f.write(f"Sample media data for {media_file}".encode())

        print(f"Created {len(media)} media files")

    def create_sample_archives(self):
        """Create sample archive files"""
        print("Creating sample archive files...")

        archives = [
            "backup_database_20240315.zip",
            "project_source_code.tar.gz",
            "documents_archive_2024.rar",
            "photos_vacation_2023.zip",
            "software_installer_v2.1.zip"
        ]

        for archive in archives:
            file_path = self.base_path / archive
            with open(file_path, 'wb') as f:
                # Create minimal archive headers
                if archive.endswith('.zip'):
                    f.write(b'PK\x03\x04')  # ZIP header
                elif archive.endswith('.rar'):
                    f.write(b'Rar!\x1a\x07\x00')  # RAR header
                f.write(f"Sample archive data for {archive}".encode())

        print(f"Created {len(archives)} archive files")

    def create_files_with_dates(self):
        """Create files with various modification dates"""
        print("Creating files with different modification dates...")

        # Create files with dates from the past year
        for i in range(10):
            days_ago = random.randint(1, 365)
            past_date = datetime.now() - timedelta(days=days_ago)

            filename = f"old_file_{past_date.strftime('%Y%m%d')}_{i+1}.txt"
            file_path = self.base_path / filename

            with open(file_path, 'w') as f:
                f.write(f"File created on: {past_date}\nThis is file number {i+1}")

            # Set the file's modification time
            timestamp = past_date.timestamp()
            os.utime(file_path, (timestamp, timestamp))

        print("Created 10 files with historical dates")

    def create_duplicate_files(self):
        """Create duplicate files for testing duplicate detection"""
        print("Creating duplicate files...")

        # Create original file
        original_content = "This is the original file content for duplicate testing."

        duplicates = [
            "original_document.txt",
            "original_document_copy.txt",
            "original_document (1).txt",
            "duplicate_test_file.txt",
            "another_copy_of_original.txt"
        ]

        for dup in duplicates:
            file_path = self.base_path / dup
            with open(file_path, 'w') as f:
                f.write(original_content)  # Same content = duplicates

        print(f"Created {len(duplicates)} duplicate files")

    def create_messy_filenames(self):
        """Create files with messy/inconsistent naming"""
        print("Creating files with messy naming patterns...")

        messy_files = [
            "Document without extension",
            "FILE WITH SPACES AND CAPS.TXT",
            "file.with.multiple.dots.pdf",
            "INVOICE#123@2024!.xlsx",
            "report    with    extra    spaces.docx",
            "file-with-dashes_and_underscores.txt",
            "混合文字file.pdf",  # Mixed language
            "file(with)parentheses[and]brackets.jpg"
        ]

        for messy in messy_files:
            file_path = self.base_path / messy
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Content for messy filename: {messy}")
            except OSError:
                # Skip files with invalid characters for the OS
                print(f"Skipped invalid filename: {messy}")
                continue

        print("Created files with messy naming patterns")

    def create_all_samples(self):
        """Create all types of sample files"""
        print("CREATING SAMPLE FILES FOR FILE ORGANIZATION TESTING")
        print("=" * 60)

        self.create_sample_documents()
        self.create_sample_images()
        self.create_sample_media()
        self.create_sample_archives()
        self.create_files_with_dates()
        self.create_duplicate_files()
        self.create_messy_filenames()

        # Count total files created
        total_files = len(list(self.base_path.glob('*')))
        total_size = sum(f.stat().st_size for f in self.base_path.glob('*') if f.is_file())

        print("\n" + "=" * 60)
        print("SAMPLE FILE CREATION COMPLETED!")
        print("=" * 60)
        print(f"Total files created: {total_files}")
        print(f"Total size: {total_size / 1024:.2f} KB")
        print(f"Location: {self.base_path}")
        print("\nThese files can now be used to test:")
        print("- File type organization")
        print("- Duplicate file detection")
        print("- Date-based archiving")
        print("- Filename cleanup and standardization")


def main():
    """Main function to create sample files"""
    # Use sample_files directory
    sample_path = Path(__file__).parent.parent / 'sample_files'

    creator = SampleFileCreator(sample_path)
    creator.create_all_samples()


if __name__ == "__main__":
    main()