from fastapi import APIRouter

router = APIRouter(
    prefix="/checks",
    tags=["pindora_check"],
    responses={404: {"description": "Not found"}},
)

@router.post("/kya_ho_raha_hai")
async def process_text():
    
    return {
        "status": "success",
        "message": f"kaam chal raha hai"
    }
