"""Task B3: Health + root info."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "service": "fitness-tracker-api"}


@router.get("/")
def root():
    return {"message": "Personal Fitness Tracker API", "docs": "/docs"}
