from fastapi import APIRouter

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

@router.get("/")
def root():
    return "expense root "