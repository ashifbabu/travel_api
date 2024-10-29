from fastapi import APIRouter

router = APIRouter()

@router.get("/cars/search")
async def search_cars():
    return {"message": "Car rental search endpoint"}