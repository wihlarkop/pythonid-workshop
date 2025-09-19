"""
Image Processing API
FastAPI application for image upload, resize, and grayscale conversion
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import io
from pathlib import Path
import os

from image_processor import image_processor

# Pydantic models
class ImageUploadResponse(BaseModel):
    """Response model for image upload"""
    success: bool
    message: str
    original_filename: str
    processed_filename: str
    processed_path: str
    original_size: dict
    processed_size: dict
    file_size_bytes: int
    processing_applied: list
    download_url: str

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool
    error: str
    details: Optional[str] = None

class ImageInfo(BaseModel):
    """Image information model"""
    format: str
    mode: str
    size: dict
    has_transparency: bool

# Create FastAPI app
app = FastAPI(
    title="Image Processing API",
    description="Upload images to automatically resize to 300x300 and convert to grayscale",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

@app.get("/", response_model=dict)
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Image Processing API",
        "description": "Upload images to resize to 300x300 and convert to grayscale",
        "endpoints": {
            "upload": "/upload-image",
            "download": "/download/{filename}",
            "info": "/image-info",
            "docs": "/docs"
        },
        "supported_formats": ["JPEG", "PNG", "GIF", "BMP", "WebP"],
        "max_file_size": "10MB",
        "processing": "Resize to 300x300 + Grayscale conversion"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    processed_dir = Path("processed")
    return {
        "status": "healthy",
        "processed_directory_exists": processed_dir.exists(),
        "processed_files_count": len(list(processed_dir.glob("*"))) if processed_dir.exists() else 0
    }

@app.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload and process an image
    
    - Accepts image files (JPEG, PNG, GIF, BMP, WebP)
    - Resizes to 300x300 pixels (maintaining aspect ratio)
    - Converts to grayscale
    - Saves in processed/ folder
    - Returns file path and metadata
    """
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Check file extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check content type
    if not image_processor.is_valid_image_format(file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid content type: {file.content_type}"
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Process image
        image_bytes = io.BytesIO(content)
        result = image_processor.process_image(image_bytes, file.filename)
        
        if not result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image processing failed: {result['error']}"
            )
        
        # Create download URL
        download_url = f"/download/{result['processed_filename']}"
        
        return ImageUploadResponse(
            success=True,
            message="Image processed successfully",
            original_filename=result['original_filename'],
            processed_filename=result['processed_filename'],
            processed_path=result['processed_path'],
            original_size=result['original_size'],
            processed_size=result['processed_size'],
            file_size_bytes=result['file_size_bytes'],
            processing_applied=result['processing_applied'],
            download_url=download_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/download/{filename}")
async def download_processed_image(filename: str):
    """
    Download a processed image
    
    - **filename**: Name of the processed image file
    """
    file_path = Path("processed") / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return FileResponse(
        path=file_path,
        media_type='image/jpeg',
        filename=filename
    )

@app.post("/image-info", response_model=ImageInfo)
async def get_image_info(file: UploadFile = File(...)):
    """
    Get information about an image without processing it
    
    - Returns format, dimensions, and other metadata
    - Does not save or modify the image
    """
    
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    try:
        content = await file.read()
        image_bytes = io.BytesIO(content)
        
        info = image_processor.get_image_info(image_bytes)
        
        if 'error' in info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not read image: {info['error']}"
            )
        
        return ImageInfo(
            format=info['format'],
            mode=info['mode'],
            size=info['size'],
            has_transparency=info['has_transparency']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading image: {str(e)}"
        )

@app.get("/processed-files")
async def list_processed_files():
    """
    List all processed image files
    
    Returns a list of all files in the processed directory
    """
    processed_dir = Path("processed")
    
    if not processed_dir.exists():
        return {"files": [], "count": 0}
    
    files = []
    for file_path in processed_dir.glob("*"):
        if file_path.is_file():
            stat = file_path.stat()
            files.append({
                "filename": file_path.name,
                "size_bytes": stat.st_size,
                "created": stat.st_ctime,
                "download_url": f"/download/{file_path.name}"
            })
    
    # Sort by creation time (newest first)
    files.sort(key=lambda x: x['created'], reverse=True)
    
    return {
        "files": files,
        "count": len(files)
    }

@app.delete("/cleanup")
async def cleanup_old_files():
    """
    Clean up old processed files
    
    Removes old files if there are more than 100 processed images
    """
    try:
        image_processor.cleanup_old_files(max_files=100)
        
        # Count remaining files
        processed_dir = Path("processed")
        remaining_count = len(list(processed_dir.glob("*"))) if processed_dir.exists() else 0
        
        return {
            "success": True,
            "message": "Cleanup completed",
            "remaining_files": remaining_count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cleanup failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)