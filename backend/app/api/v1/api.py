from app.api.v1.endpoints import subscribers, events, newsletters, collector, analytics

api_router = APIRouter()
api_router.include_router(subscribers.router, prefix="/subscribers", tags=["subscribers"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(newsletters.router, prefix="/newsletters", tags=["newsletters"])
api_router.include_router(collector.router, prefix="/collector", tags=["collector"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
