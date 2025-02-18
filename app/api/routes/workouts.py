from typing import Annotated

from fastapi import Query, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from pydantic.types import UUID4

from app.dependencies import CurrentUser, SessionDep
from app.schemas.base import AppPaginatedResponse, AppResponse
from app.schemas.workouts import (
    WorkoutCreate,
    WorkoutPublic,
    WorkoutQuery,
    WorkoutUpdate,
)
from app.crud import workouts as workout_crud
from app.crud import goals as goal_crud


router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("/")
async def get_all_workouts(
    session: SessionDep, user: CurrentUser, query: Annotated[WorkoutQuery, Query()]
) -> AppPaginatedResponse[WorkoutPublic]:
    workouts = await workout_crud.get_all_workouts(
        session, user, query.page, query.limit, query.exercise
    )
    total = await workout_crud.total_workouts(session, user)
    return AppPaginatedResponse(
        result=[WorkoutPublic.model_validate(workout) for workout in workouts],
        page=query.page,
        limit=query.limit,
        total=total,
        status=status.HTTP_200_OK,
    )


@router.get("/{workout_id}")
async def get_workout(
    session: SessionDep, user: CurrentUser, workout_id: UUID4
) -> AppResponse[WorkoutPublic]:
    workout = await workout_crud.get_workout(session, user, workout_id)
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Workout not exist",
            },
        )

    return AppResponse(
        data=WorkoutPublic.model_validate(workout),
        status=status.HTTP_200_OK,
    )


@router.post("/")
async def create_workout(
    session: SessionDep, user: CurrentUser, workout_data: WorkoutCreate
) -> AppResponse:
    if workout_data.goal_id:
        goal = await goal_crud.get_goal_by_id(session, user, workout_data.goal_id)
        if goal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Goal not exist",
                },
            )

    await workout_crud.create_workout(session, user, workout_data)

    return AppResponse(
        message="Created Successfully",
        status=status.HTTP_201_CREATED,
    )


@router.patch("/{workout_id}")
async def update_workout(
    session: SessionDep,
    user: CurrentUser,
    workout_id: UUID4,
    workout_data: WorkoutUpdate,
) -> AppResponse:
    workout = await workout_crud.get_workout(session, user, workout_id)
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Workout not exist",
            },
        )

    if workout_data.goal_id:
        goal = await goal_crud.get_goal_by_id(session, user, workout_data.goal_id)
        if goal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Goal not exist",
                },
            )

    await workout_crud.update_workout(session, workout, workout_data)

    return AppResponse(
        message="Updated Successfully",
        status=status.HTTP_200_OK,
    )


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    session: SessionDep, user: CurrentUser, workout_id: UUID4
) -> None:
    workout = await workout_crud.get_workout(session, user, workout_id)
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Workout not exist",
            },
        )

    await workout_crud.delete_workout(session, workout)
