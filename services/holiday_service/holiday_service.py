from fastapi import APIRouter

router = APIRouter()


@router.get("/holidays/search")
async def search_holidays():
    return {"message": "Holiday search endpoint"}
