from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import analytics_service
from typing import Any

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_data(db: Session = Depends(get_db)) -> Any:
    """
    Get aggregated dashboard statistics.
    """
    return analytics_service.get_dashboard_stats(db)
