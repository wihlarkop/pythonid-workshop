# Image Processing API Workshop

A FastAPI application for image upload, automatic resizing to 300x300, and grayscale conversion using Pillow.

## 🎯 Workshop Overview

Learn to build file upload APIs with FastAPI and image processing:
- File upload handling with FastAPI
- Image processing with Pillow (PIL)
- Error handling for file operations
- File validation and security
- Image format conversion and manipulation

## 🚀 Quick Start

```bash
# Navigate to project
cd pythonid-workshop

# Start the API server
uv run image-processing-api/src/main.py

# API will be available at:
# - Main API: http://localhost:8001
# - Interactive docs: http://localhost:8001/docs
# - Alternative docs: http://localhost:8001/redoc
```

## 📁 Project Structure

```
image-processing-api/
├── src/
│   ├── main.py              # FastAPI application with upload endpoints
│   └── image_processor.py   # Pillow image processing functions
├── processed/               # Output directory for processed images
├── uploads/                 # Temporary upload storage (optional)
├── examples/               # Sample images for testing
└── README.md
```

## 🖼️ Image Processing Pipeline

1. **Upload**: Accept image file via `/upload-image` endpoint
2. **Validate**: Check file type, size, and format
3. **Resize**: Resize to 300x300 pixels (maintaining aspect ratio)
4. **Convert**: Convert to grayscale
5. **Save**: Store in `processed/` folder with unique filename
6. **Response**: Return file path and metadata

## 📊 Supported Features

### Image Formats
- JPEG/JPG
- PNG (with transparency handling)
- GIF
- BMP
- WebP

### Processing Operations
- **Resize to 300x300**: Maintains aspect ratio, adds white padding if needed
- **Grayscale Conversion**: Full color to grayscale transformation
- **Format Standardization**: Output as high-quality JPEG

### File Management
- Unique filename generation (timestamp + UUID)
- File size validation (max 10MB)
- Automatic cleanup of old files
- Thread-safe operations

## 🛠 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and API info |
| GET | `/health` | Health check |
| POST | `/upload-image` | Upload and process image |
| GET | `/download/{filename}` | Download processed image |
| POST | `/image-info` | Get image metadata without processing |
| GET | `/processed-files` | List all processed files |
| DELETE | `/cleanup` | Clean up old files |

## 📝 Example Usage

### 1. Upload and Process Image

**Using curl:**
```bash
curl -X POST "http://localhost:8001/upload-image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-image.jpg"
```

**Response:**
```json
{
  "success": true,
  "message": "Image processed successfully",
  "original_filename": "your-image.jpg",
  "processed_filename": "processed_20241215_143022_a1b2c3d4.jpg",
  "processed_path": "processed/processed_20241215_143022_a1b2c3d4.jpg",
  "original_size": {"width": 1920, "height": 1080},
  "processed_size": {"width": 300, "height": 300},
  "file_size_bytes": 45678,
  "processing_applied": ["resize_to_300x300", "convert_to_grayscale"],
  "download_url": "/download/processed_20241215_143022_a1b2c3d4.jpg"
}
```

### 2. Download Processed Image
```bash
curl "http://localhost:8001/download/processed_20241215_143022_a1b2c3d4.jpg" \
  --output processed_image.jpg
```

### 3. Get Image Information
```bash
curl -X POST "http://localhost:8001/image-info" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-image.jpg"
```

### 4. List Processed Files
```bash
curl "http://localhost:8001/processed-files"
```

## 🧪 Testing with Interactive Docs

1. Go to http://localhost:8001/docs
2. Navigate to `/upload-image` endpoint
3. Click "Try it out"
4. Choose an image file
5. Click "Execute"
6. View the response with processed image details
7. Use the download URL to get the processed image

## 🎓 Learning Objectives

### FastAPI File Handling
- **File Upload**: Using `UploadFile` and `File()`
- **Content Validation**: MIME type and extension checking
- **File Size Limits**: Preventing large file uploads
- **Async File Operations**: Non-blocking file processing

### Image Processing with Pillow
- **Image Loading**: From bytes and file objects
- **Format Conversion**: RGB, RGBA, grayscale modes
- **Resizing Algorithms**: Lanczos resampling for quality
- **Aspect Ratio**: Maintaining proportions with padding
- **File Saving**: Quality settings and format options

### Error Handling
- **File Validation Errors**: Invalid formats, too large
- **Processing Errors**: Corrupted images, memory issues
- **HTTP Status Codes**: Proper error responses
- **Exception Handling**: Graceful failure management

## 🔧 Advanced Features

### Smart Resizing
```python
def resize_image(self, image: Image.Image, size: Tuple[int, int] = (300, 300)):
    # Maintains aspect ratio
    # Adds white padding to reach exact dimensions
    # Uses high-quality Lanczos resampling
```

### Unique Filename Generation
```python
def generate_unique_filename(self, original_filename: str):
    # Format: processed_YYYYMMDD_HHMMSS_UNIQUEID.jpg
    # Prevents filename conflicts
    # Maintains original extension
```

### File Cleanup
```python
def cleanup_old_files(self, max_files: int = 100):
    # Automatically removes oldest files
    # Prevents disk space issues
    # Configurable retention policy
```

## 💡 Workshop Exercises

### Exercise 1: Basic Upload
1. Start the API server
2. Upload different image formats (PNG, JPEG, GIF)
3. Check the processed results
4. Download and compare original vs processed

### Exercise 2: Error Testing
1. Try uploading non-image files
2. Upload very large images
3. Test with corrupted image files
4. Observe error responses

### Exercise 3: Batch Processing
1. Upload multiple images
2. List all processed files
3. Download several processed images
4. Test the cleanup functionality

### Exercise 4: Image Analysis
1. Use `/image-info` to analyze images before processing
2. Compare original and processed image metadata
3. Test with images of different sizes and formats

## 🚀 Extensions & Next Steps

### Easy Extensions
- Add more image sizes (thumbnail, medium, large)
- Add different filters (sepia, blur, sharpen)
- Add image rotation and flip operations
- Add watermark functionality

### Advanced Extensions
- Add authentication and user management
- Implement image galleries and albums
- Add batch processing for multiple files
- Add image format conversion options
- Implement image compression settings

### Production Considerations
- Use cloud storage (AWS S3, Google Cloud Storage)
- Add image optimization and compression
- Implement rate limiting
- Add image metadata extraction (EXIF data)
- Add virus scanning for uploaded files

## 🧩 Key Code Patterns

### File Upload Handling
```python
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Validate file
    content = await file.read()
    # Process content
    return response
```

### Image Processing Pipeline
```python
# Open image
image = Image.open(image_bytes)

# Convert mode if needed
if image.mode != 'RGB':
    image = image.convert('RGB')

# Resize with aspect ratio
resized = self.resize_image(image, (300, 300))

# Convert to grayscale
grayscale = ImageOps.grayscale(resized)

# Save with quality
grayscale.save(path, 'JPEG', quality=90)
```

## 📚 Key Technologies

- **FastAPI**: Modern web framework for APIs
- **Pillow (PIL)**: Python Imaging Library for image processing
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the application

## 🎯 Workshop Outcomes

After completing this workshop, participants will understand:

1. **File Upload APIs**: Building robust file upload endpoints
2. **Image Processing**: Using Pillow for image manipulation
3. **Error Handling**: Proper validation and error responses
4. **File Management**: Organizing and cleaning up uploaded files
5. **API Documentation**: Leveraging FastAPI's automatic docs

Perfect for learning file handling and image processing in web APIs! 📸⚡

---

**Ready to process images with FastAPI! 🚀**