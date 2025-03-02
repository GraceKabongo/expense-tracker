from fastapi import APIRouter

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get("/")
def root():
    return "categorie root "