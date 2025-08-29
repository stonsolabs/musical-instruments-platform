from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from ..database import get_db
from ..models import OpenAIBatch, Product
from ..services.azure_openai_batch import AzureOpenAIBatchProcessor

router = APIRouter(prefix="/batch", tags=["batch-processing"])

# Global processor instance
batch_processor = AzureOpenAIBatchProcessor()


@router.post("/create")
async def create_batch(
    category_limit: int = 3,
    background_tasks: BackgroundTasks = None
) -> Dict[str, Any]:
    """Create a new batch for AI content generation."""
    try:
        # Generate batch ID
        batch_id = str(uuid.uuid4())
        
        # Get products for batch processing
        products = await batch_processor.get_products_for_batch(category_limit)
        
        if not products:
            raise HTTPException(status_code=404, detail="No products found for batch processing")
        
        # Create batch file
        filepath = await batch_processor.create_batch_file(products, batch_id)
        
        # Create batch record in database
        async with get_db() as db:
            batch_record = {
                "batch_id": batch_id,
                "filename": filepath,
                "product_count": len(products),
                "status": "pending",
                "created_at": datetime.utcnow()
            }
            
            await db.execute(insert(OpenAIBatch).values(**batch_record))
            await db.commit()
        
        return {
            "batch_id": batch_id,
            "filepath": filepath,
            "product_count": len(products),
            "status": "created"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create batch: {str(e)}")


@router.post("/submit/{batch_id}")
async def submit_batch(batch_id: str) -> Dict[str, Any]:
    """Submit a batch to Azure OpenAI for processing."""
    try:
        # Get batch record
        async with get_db() as db:
            result = await db.execute(
                select(OpenAIBatch).where(OpenAIBatch.batch_id == batch_id)
            )
            batch_record = result.scalar_one_or_none()
            
            if not batch_record:
                raise HTTPException(status_code=404, detail="Batch not found")
            
            if batch_record.status != "pending":
                raise HTTPException(status_code=400, detail=f"Batch is in {batch_record.status} status")
        
        # Submit batch to Azure OpenAI
        openai_job_id = await batch_processor.submit_batch(batch_record.filename, batch_id)
        
        return {
            "batch_id": batch_id,
            "openai_job_id": openai_job_id,
            "status": "submitted"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit batch: {str(e)}")


@router.get("/status/{batch_id}")
async def get_batch_status(batch_id: str) -> Dict[str, Any]:
    """Get the status of a batch job."""
    try:
        status = await batch_processor.check_batch_status(batch_id)
        return {
            "batch_id": batch_id,
            **status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get batch status: {str(e)}")


@router.post("/process-results/{batch_id}")
async def process_batch_results(batch_id: str) -> Dict[str, Any]:
    """Download and process batch results."""
    try:
        results = await batch_processor.download_and_process_results(batch_id)
        return {
            "batch_id": batch_id,
            **results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process batch results: {str(e)}")


@router.post("/create-test")
async def create_test_batch(products_per_category: int = 5) -> Dict[str, Any]:
    """Create a test batch with 5 products from each category for testing."""
    try:
        # Generate batch ID
        batch_id = str(uuid.uuid4())
        
        # Get products for test batch
        products = await batch_processor.create_test_batch(products_per_category)
        
        if not products:
            raise HTTPException(status_code=404, detail="No products found for test batch")
        
        # Create batch file
        filepath = await batch_processor.create_batch_file(products, batch_id)
        
        # Create batch record in database
        async with get_db() as db:
            batch_record = {
                "batch_id": batch_id,
                "filename": filepath,
                "product_count": len(products),
                "status": "pending",
                "created_at": datetime.utcnow()
            }
            
            await db.execute(insert(OpenAIBatch).values(**batch_record))
            await db.commit()
        
        return {
            "batch_id": batch_id,
            "filepath": filepath,
            "product_count": len(products),
            "status": "created",
            "type": "test"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create test batch: {str(e)}")


@router.get("/list")
async def list_batches() -> Dict[str, Any]:
    """List all batches."""
    try:
        async with get_db() as db:
            result = await db.execute(
                select(OpenAIBatch).order_by(OpenAIBatch.created_at.desc())
            )
            batches = result.scalars().all()
            
            batch_list = []
            for batch in batches:
                batch_list.append({
                    "batch_id": batch.batch_id,
                    "filename": batch.filename,
                    "product_count": batch.product_count,
                    "status": batch.status,
                    "openai_job_id": batch.openai_job_id,
                    "created_at": batch.created_at.isoformat() if batch.created_at else None,
                    "completed_at": batch.completed_at.isoformat() if batch.completed_at else None,
                    "error_message": batch.error_message
                })
            
            return {
                "batches": batch_list,
                "total_count": len(batch_list)
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list batches: {str(e)}")


@router.get("/products/status")
async def get_products_processing_status() -> Dict[str, Any]:
    """Get processing status of all products."""
    try:
        async with get_db() as db:
            # Count products by processing status
            pending_result = await db.execute(
                select(Product).where(Product.openai_processing_status == 'pending')
            )
            pending_count = len(pending_result.scalars().all())
            
            processing_result = await db.execute(
                select(Product).where(Product.openai_processing_status == 'processing')
            )
            processing_count = len(processing_result.scalars().all())
            
            completed_result = await db.execute(
                select(Product).where(Product.openai_processing_status == 'completed')
            )
            completed_count = len(completed_result.scalars().all())
            
            failed_result = await db.execute(
                select(Product).where(Product.openai_processing_status == 'failed')
            )
            failed_count = len(failed_result.scalars().all())
            
            total_result = await db.execute(select(Product))
            total_count = len(total_result.scalars().all())
            
            return {
                "total_products": total_count,
                "pending": pending_count,
                "processing": processing_count,
                "completed": completed_count,
                "failed": failed_count
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get products status: {str(e)}")


@router.post("/full-pipeline/{batch_id}")
async def run_full_pipeline(batch_id: str) -> Dict[str, Any]:
    """Run the full batch processing pipeline: create, submit, and process results."""
    try:
        # Step 1: Submit batch
        submit_result = await submit_batch(batch_id)
        
        # Step 2: Wait a bit and check status
        import asyncio
        await asyncio.sleep(5)
        
        # Step 3: Check status
        status_result = await get_batch_status(batch_id)
        
        return {
            "batch_id": batch_id,
            "submit_result": submit_result,
            "status_result": status_result,
            "message": "Batch submitted successfully. Use /status/{batch_id} to check progress and /process-results/{batch_id} when completed."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run full pipeline: {str(e)}")
