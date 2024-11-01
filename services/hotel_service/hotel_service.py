from fastapi import APIRouter

router = APIRouter()


@router.get("/hotels/search")
async def search_hotels():
    return {"message": "Hotel search endpoint"}
