from fastapi import APIRouter

from .routes import auth, goals, workouts, utils

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(goals.router)
api_router.include_router(workouts.router)
api_router.include_router(utils.router)
