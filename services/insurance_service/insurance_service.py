from fastapi import APIRouter

router = APIRouter()

@router.get("/insurance/search")
async def search_insurance():
    return {"message": "Insurance search endpoint"}