from fastapi import APIRouter

router = APIRouter()


@router.get("/buses/search")
async def search_buses():
    return {"message": "Bus search endpoint"}
