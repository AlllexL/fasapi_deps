from fastapi import APIRouter

from core.config import settings

from .dependencies_examples import router as dep_router
from .users import router as users_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(
    dep_router,
    prefix=settings.api.v1.deps,
)
