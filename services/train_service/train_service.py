from fastapi import APIRouter

router = APIRouter()

@router.get("/trains/search")
async def search_trains():
    return {"message": "Train search endpoint"}