"""FastAPI application for PPT Reviewer Agent."""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from config import settings

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    """Root endpoint."""
    return {
        "message": "Welcome to PPT Reviewer Agent API",
        "version": settings.api_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/analyze")
async def analyze_presentation(file: UploadFile = File(...)):
    """Analyze PowerPoint presentation."""
    try:
        # Validate file type
        if not file.filename.endswith(('.pptx', '.ppt')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only .pptx and .ppt files are supported."
            )
        
        # Validate file size
        contents = await file.read()
        file_size_mb = len(contents) / (1024 * 1024)
        if file_size_mb > settings.max_file_size_mb:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {settings.max_file_size_mb}MB."
            )
        
        logger.info(f"Received file: {file.filename} ({file_size_mb:.2f}MB)")
        
        # TODO: Integrate with ppt_parser and ai_analyzer
        return {
            "status": "processing",
            "filename": file.filename,
            "message": "Analysis in progress..."
        }
    
    except Exception as e:
        logger.error(f"Error analyzing file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/report/{job_id}")
async def get_report(job_id: str, format: str = "json"):
    """Retrieve analysis report."""
    try:
        # TODO: Retrieve report from database/cache
        return {
            "job_id": job_id,
            "status": "completed",
            "overall_score": 78,
            "message": "Report retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error retrieving report: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
