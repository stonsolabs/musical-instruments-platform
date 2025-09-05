"""
API endpoints for instrument requests
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
import logging

from app.database import get_db
from app.api.dependencies import get_api_key

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models
class InstrumentRequestCreate(BaseModel):
    brand: str = Field(..., max_length=100, description="Instrument brand")
    name: str = Field(..., max_length=200, description="Instrument name")
    model: Optional[str] = Field(None, max_length=100, description="Instrument model/variant")
    category: str = Field(..., max_length=100, description="Instrument category")
    storeLink: Optional[str] = Field(None, description="Store link to the instrument")
    additionalInfo: Optional[str] = Field(None, description="Additional information")
    user_email: Optional[str] = Field(None, max_length=255, description="User email (optional)")
    
    @validator('brand', 'name', 'category')
    def validate_required_fields(cls, v):
        if not v or not v.strip():
            raise ValueError('This field is required')
        return v.strip()
    
    @validator('storeLink')
    def validate_store_link(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Store link must be a valid URL')
        return v

class InstrumentRequestResponse(BaseModel):
    id: int
    brand: str
    name: str
    model: Optional[str]
    category: str
    store_link: Optional[str]
    additional_info: Optional[str]
    status: str
    user_email: Optional[str]
    priority: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InstrumentRequestUpdate(BaseModel):
    status: Optional[str] = Field(None, regex="^(pending|reviewing|approved|rejected|completed)$")
    priority: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None

@router.post("/instrument-requests", response_model=dict)
async def create_instrument_request(
    request_data: InstrumentRequestCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Create a new instrument request"""
    
    try:
        # Get user IP address
        user_ip = request.client.host
        
        # Insert the new instrument request
        query = """
        INSERT INTO instrument_requests (
            brand, name, model, category, store_link, additional_info, 
            user_email, user_ip, created_at, updated_at
        ) VALUES (
            :brand, :name, :model, :category, :store_link, :additional_info,
            :user_email, :user_ip, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        ) RETURNING id
        """
        
        result = await db.execute(text(query), {
            'brand': request_data.brand,
            'name': request_data.name,
            'model': request_data.model,
            'category': request_data.category,
            'store_link': request_data.storeLink,
            'additional_info': request_data.additionalInfo,
            'user_email': request_data.user_email,
            'user_ip': user_ip
        })
        
        await db.commit()
        
        request_id = result.scalar()
        
        logger.info(f"Created instrument request {request_id} for {request_data.brand} {request_data.name}")
        
        return {
            "id": request_id,
            "message": "Instrument request submitted successfully",
            "status": "pending"
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create instrument request: {e}")
        raise HTTPException(status_code=500, detail="Failed to create instrument request")

@router.get("/instrument-requests", response_model=List[InstrumentRequestResponse])
async def get_instrument_requests(
    status: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get instrument requests with optional filtering"""
    
    try:
        # Build the query
        where_clauses = []
        params = {}
        
        if status:
            where_clauses.append("status = :status")
            params['status'] = status
            
        if category:
            where_clauses.append("category = :category")
            params['category'] = category
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
        SELECT 
            id, brand, name, model, category, store_link, additional_info,
            status, user_email, priority, created_at, updated_at
        FROM instrument_requests
        {where_clause}
        ORDER BY priority DESC, created_at DESC
        LIMIT :limit OFFSET :offset
        """
        
        params.update({'limit': limit, 'offset': offset})
        
        result = await db.execute(text(query), params)
        requests = result.fetchall()
        
        return [
            InstrumentRequestResponse(
                id=row[0],
                brand=row[1],
                name=row[2],
                model=row[3],
                category=row[4],
                store_link=row[5],
                additional_info=row[6],
                status=row[7],
                user_email=row[8],
                priority=row[9],
                created_at=row[10],
                updated_at=row[11]
            )
            for row in requests
        ]
        
    except Exception as e:
        logger.error(f"Failed to fetch instrument requests: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch instrument requests")

@router.get("/instrument-requests/{request_id}", response_model=InstrumentRequestResponse)
async def get_instrument_request(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific instrument request"""
    
    try:
        query = """
        SELECT 
            id, brand, name, model, category, store_link, additional_info,
            status, user_email, priority, created_at, updated_at
        FROM instrument_requests
        WHERE id = :request_id
        """
        
        result = await db.execute(text(query), {'request_id': request_id})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Instrument request not found")
        
        return InstrumentRequestResponse(
            id=row[0],
            brand=row[1],
            name=row[2],
            model=row[3],
            category=row[4],
            store_link=row[5],
            additional_info=row[6],
            status=row[7],
            user_email=row[8],
            priority=row[9],
            created_at=row[10],
            updated_at=row[11]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch instrument request {request_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch instrument request")

@router.put("/instrument-requests/{request_id}", response_model=dict)
async def update_instrument_request(
    request_id: int,
    update_data: InstrumentRequestUpdate,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Update an instrument request (admin only)"""
    
    try:
        # Check if request exists
        check_query = "SELECT id FROM instrument_requests WHERE id = :request_id"
        result = await db.execute(text(check_query), {'request_id': request_id})
        
        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Instrument request not found")
        
        # Build update query
        set_clauses = []
        params = {'request_id': request_id}
        
        if update_data.status is not None:
            set_clauses.append("status = :status")
            params['status'] = update_data.status
            
        if update_data.priority is not None:
            set_clauses.append("priority = :priority")
            params['priority'] = update_data.priority
            
        if update_data.notes is not None:
            set_clauses.append("notes = :notes")
            params['notes'] = update_data.notes
        
        if not set_clauses:
            raise HTTPException(status_code=400, detail="No updates provided")
        
        # Add timestamp updates based on status
        if update_data.status == 'reviewing':
            set_clauses.append("reviewed_at = CURRENT_TIMESTAMP")
        elif update_data.status == 'completed':
            set_clauses.append("completed_at = CURRENT_TIMESTAMP")
        
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        
        query = f"""
        UPDATE instrument_requests 
        SET {', '.join(set_clauses)}
        WHERE id = :request_id
        """
        
        await db.execute(text(query), params)
        await db.commit()
        
        logger.info(f"Updated instrument request {request_id}")
        
        return {"message": "Instrument request updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update instrument request {request_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update instrument request")

@router.delete("/instrument-requests/{request_id}", response_model=dict)
async def delete_instrument_request(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Delete an instrument request (admin only)"""
    
    try:
        query = "DELETE FROM instrument_requests WHERE id = :request_id"
        result = await db.execute(text(query), {'request_id': request_id})
        await db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Instrument request not found")
        
        logger.info(f"Deleted instrument request {request_id}")
        
        return {"message": "Instrument request deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete instrument request {request_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete instrument request")

@router.get("/instrument-requests/stats", response_model=dict)
async def get_instrument_requests_stats(
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get instrument requests statistics"""
    
    try:
        query = """
        SELECT 
            COUNT(*) as total_requests,
            COUNT(*) FILTER (WHERE status = 'pending') as pending_requests,
            COUNT(*) FILTER (WHERE status = 'reviewing') as reviewing_requests,
            COUNT(*) FILTER (WHERE status = 'approved') as approved_requests,
            COUNT(*) FILTER (WHERE status = 'completed') as completed_requests,
            COUNT(*) FILTER (WHERE status = 'rejected') as rejected_requests,
            COUNT(*) FILTER (WHERE created_at >= CURRENT_DATE - INTERVAL '7 days') as requests_last_week,
            COUNT(*) FILTER (WHERE created_at >= CURRENT_DATE - INTERVAL '30 days') as requests_last_month
        FROM instrument_requests
        """
        
        result = await db.execute(text(query))
        row = result.fetchone()
        
        return {
            "total_requests": row[0],
            "pending_requests": row[1],
            "reviewing_requests": row[2],
            "approved_requests": row[3],
            "completed_requests": row[4],
            "rejected_requests": row[5],
            "requests_last_week": row[6],
            "requests_last_month": row[7]
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch instrument requests stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")