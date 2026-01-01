"""Fully integrated PPT Reviewer Agent - Complete working application."""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import logging
import os
import tempfile
import uuid
from pathlib import Path
from typing import Dict

from config import settings
from ppt_parser import PowerPointParser
from ai_analyzer import AIAnalyzer
from report_generator import ReportGenerator

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Initialize components
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

# In-memory storage for analysis results (in production use database)
analysis_results: Dict[str, dict] = {}

# Initialize AI analyzer
ai_analyzer = AIAnalyzer()
report_gen = ReportGenerator()


@app.get("/")
async def read_root():
    """Root endpoint."""
    return {
        "message": "🤖 PPT Reviewer Agent - AI-Powered PowerPoint Analysis",
        "version": settings.api_version,
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.api_version}


@app.post("/api/analyze")
async def analyze_presentation(file: UploadFile = File(...)):
    """Analyze PowerPoint presentation - Main endpoint."""
    job_id = str(uuid.uuid4())
    
    try:
        # Validate file type
        if not file.filename.endswith(('.pptx', '.ppt')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only .pptx and .ppt files are supported."
            )
        
        # Read file content
        contents = await file.read()
        file_size_mb = len(contents) / (1024 * 1024)
        
        # Validate file size
        if file_size_mb > settings.max_file_size_mb:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {settings.max_file_size_mb}MB."
            )
        
        logger.info(f"[{job_id}] Received file: {file.filename} ({file_size_mb:.2f}MB)")
        
        # Save temporarily
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"{job_id}_{file.filename}")
        
        with open(temp_file, 'wb') as f:
            f.write(contents)
        
        try:
            # Parse presentation
            logger.info(f"[{job_id}] Parsing presentation...")
            parser = PowerPointParser(temp_file)
            parser.extract_all_slides()
            presentation_data = parser.get_all_analysis()
            
            logger.info(f"[{job_id}] Found {len(parser.slides_data)} slides")
            
            # Analyze with AI
            logger.info(f"[{job_id}] Starting AI analysis...")
            analysis_results_list = []
            
            for slide in parser.slides_data:
                slide_analysis = ai_analyzer.analyze_slide_content(slide)
                analysis_results_list.append(slide_analysis)
            
            # Analyze overall structure
            structure_analysis = ai_analyzer.analyze_presentation_structure(parser.slides_data)
            
            # Generate report
            logger.info(f"[{job_id}] Generating report...")
            complete_analysis = {
                "metadata": presentation_data["metadata"],
                "slides": presentation_data["slides"],
                "slide_analyses": analysis_results_list,
                "structure_analysis": structure_analysis,
            }
            
            reports = report_gen.generate_all_reports(complete_analysis)
            
            # Store results
            analysis_results[job_id] = {
                "status": "completed",
                "filename": file.filename,
                "total_slides": len(parser.slides_data),
                "analysis": complete_analysis,
                "reports": reports,
            }
            
            logger.info(f"[{job_id}] Analysis complete!")
            
            return {
                "status": "success",
                "job_id": job_id,
                "filename": file.filename,
                "total_slides": len(parser.slides_data),
                "message": "Presentation analyzed successfully",
                "data": {
                    "metadata": presentation_data["metadata"],
                    "total_slides": len(parser.slides_data),
                    "structure_analysis": structure_analysis,
                }
            }
        
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    except HTTPException as e:
        logger.error(f"[{job_id}] HTTP Error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"[{job_id}] Error analyzing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/report/{job_id}")
async def get_report(job_id: str, format: str = "json"):
    """Retrieve analysis report."""
    try:
        if job_id not in analysis_results:
            raise HTTPException(status_code=404, detail="Job not found")
        
        result = analysis_results[job_id]
        
        if format == "html":
            return FileResponse(
                content=result["reports"]["html"],
                media_type="text/html"
            )
        elif format == "markdown":
            return FileResponse(
                content=result["reports"]["markdown"],
                media_type="text/plain"
            )
        else:  # json (default)
            return JSONResponse(content={
                "status": result["status"],
                "filename": result["filename"],
                "total_slides": result["total_slides"],
                "analysis": result["analysis"],
                "report": result["reports"]["json"]
            })
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving report: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving report")


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get analysis status."""
    if job_id not in analysis_results:
        return {"status": "not found"}
    
    return {
        "status": analysis_results[job_id]["status"],
        "filename": analysis_results[job_id]["filename"],
        "total_slides": analysis_results[job_id]["total_slides"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
