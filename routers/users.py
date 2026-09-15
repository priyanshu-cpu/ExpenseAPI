from fastapi import APIRouter

router = APIRouter(prefix="/users")

@router.get("/")
def home():
    pass