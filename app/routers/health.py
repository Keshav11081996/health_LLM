from fastapi import APIRouter

router = APIRouter()

@router.get("/check")
def health_check():
    return {
        "status": 200
    }