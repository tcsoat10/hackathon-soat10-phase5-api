from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Checks the health of the application.",
    response_description="Application is healthy.",
)
async def health_check():
    return {"status": "ok"}

