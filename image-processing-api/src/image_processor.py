"""
Image Processing Functions
Handles image resizing and grayscale conversion using Pillow
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageOps


class ImageProcessor:
    """Image processing utilities for the API"""

    def __init__(self, processed_dir: str = "processed"):
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(exist_ok=True)

        # Supported image formats
        self.supported_formats = {
            'image/jpeg', 'image/jpg', 'image/png',
            'image/gif', 'image/bmp', 'image/webp'
        }

    def is_valid_image_format(self, content_type: str) -> bool:
        """Check if the uploaded file is a supported image format"""
        return content_type.lower() in self.supported_formats

    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename for processed image"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]

        # Extract extension from original filename
        original_path = Path(original_filename)
        extension = original_path.suffix.lower()

        # Default to .jpg if no extension
        if not extension:
            extension = '.jpg'

        return f"processed_{timestamp}_{unique_id}{extension}"

    def resize_image(self, image: Image.Image, size: Tuple[int, int] = (300, 300)) -> Image.Image:
        """
        Resize image to specified size while maintaining aspect ratio
        
        Args:
            image: PIL Image object
            size: Target size as (width, height)
            
        Returns:
            Resized PIL Image
        """
        # Calculate aspect ratio
        original_width, original_height = image.size
        target_width, target_height = size

        # Calculate scaling factor to maintain aspect ratio
        scale_width = target_width / original_width
        scale_height = target_height / original_height
        scale = min(scale_width, scale_height)

        # Calculate new dimensions
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        # Resize image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create a new image with target size and paste resized image in center
        final_image = Image.new('RGB', size, color='white')
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        final_image.paste(resized_image, (paste_x, paste_y))

        return final_image

    def convert_to_grayscale(self, image: Image.Image) -> Image.Image:
        """
        Convert image to grayscale
        
        Args:
            image: PIL Image object
            
        Returns:
            Grayscale PIL Image
        """
        return ImageOps.grayscale(image)

    def process_image(self, image_bytes: bytes, original_filename: str) -> dict:
        """
        Complete image processing pipeline: resize and convert to grayscale
        
        Args:
            image_bytes: Raw image bytes
            original_filename: Original filename for reference
            
        Returns:
            dict: Processing results with file paths and metadata
        """
        try:
            # Open image from bytes
            image = Image.open(image_bytes)

            # Convert to RGB if necessary (handles RGBA, P mode images)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Get original dimensions
            original_width, original_height = image.size

            # Resize image to 300x300
            resized_image = self.resize_image(image, (300, 300))

            # Convert to grayscale
            grayscale_image = self.convert_to_grayscale(resized_image)

            # Generate unique filename
            processed_filename = self.generate_unique_filename(original_filename)
            processed_path = self.processed_dir / processed_filename

            # Save processed image
            grayscale_image.save(processed_path, 'JPEG', quality=90)

            return {
                'success': True,
                'original_filename': original_filename,
                'processed_filename': processed_filename,
                'processed_path': str(processed_path),
                'original_size': {'width': original_width, 'height': original_height},
                'processed_size': {'width': 300, 'height': 300},
                'file_size_bytes': processed_path.stat().st_size,
                'processing_applied': ['resize_to_300x300', 'convert_to_grayscale']
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'original_filename': original_filename
            }

    def get_image_info(self, image_bytes: bytes) -> dict:
        """
        Get metadata about an image without processing it
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            dict: Image metadata
        """
        try:
            image = Image.open(image_bytes)

            return {
                'format': image.format,
                'mode': image.mode,
                'size': {'width': image.width, 'height': image.height},
                'has_transparency': image.mode in ('RGBA', 'LA') or 'transparency' in image.info
            }
        except Exception as e:
            return {'error': str(e)}

    def cleanup_old_files(self, max_files: int = 100):
        """
        Clean up old processed files to prevent disk space issues
        
        Args:
            max_files: Maximum number of files to keep
        """
        try:
            # Get all files in processed directory
            files = list(self.processed_dir.glob('*'))

            if len(files) <= max_files:
                return

            # Sort by modification time (oldest first)
            files.sort(key=lambda x: x.stat().st_mtime)

            # Remove oldest files
            files_to_remove = files[:-max_files]
            for file_path in files_to_remove:
                file_path.unlink()

        except Exception as e:
            print(f"Error during cleanup: {e}")


# Global processor instance
image_processor = ImageProcessor()
