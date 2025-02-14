from fastapi import APIRouter
from apps.tasks.views import router as task_router

router = APIRouter()
router.include_router(task_router)
