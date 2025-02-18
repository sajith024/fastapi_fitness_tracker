from typing import Annotated

from fastapi import Query, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from pydantic.types import UUID4

from app.dependencies import CurrentUser, SessionDep
from app.schemas.base import AppPaginatedResponse, AppResponse, PaginationQuery
from app.crud import goals as goal_crud
from app.schemas.goals import GoalCreate, GoalPublic, GoalUpdate


router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/")
async def get_all_goals(
    session: SessionDep, user: CurrentUser, query: Annotated[PaginationQuery, Query()]
) -> AppPaginatedResponse[GoalPublic]:
    goals = await goal_crud.get_all_goals(session, user, query.page, query.limit)
    total = await goal_crud.total_goals(session, user)
    return AppPaginatedResponse(
        result=[GoalPublic.model_validate(goal) for goal in goals],
        page=query.page,
        limit=query.limit,
        total=total,
        status=status.HTTP_200_OK,
    )


@router.post("/")
async def create_goal(
    session: SessionDep, user: CurrentUser, goal_data: GoalCreate
) -> AppResponse:
    await goal_crud.create_goal(session, user, goal_data)
    return AppResponse(
        message="Created Successfully",
        status=status.HTTP_201_CREATED,
    )


@router.patch("/{goal_id}")
async def update_goal(
    session: SessionDep, user: CurrentUser, goal_id: UUID4, goal_data: GoalUpdate
) -> AppResponse:
    goal = await goal_crud.get_goal_by_id(session, user, goal_id)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Goal not exist",
            },
        )

    await goal_crud.update_goal(session, goal, goal_data)
    return AppResponse(
        message="Updated Successfully",
        status=status.HTTP_200_OK,
    )


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(session: SessionDep, user: CurrentUser, goal_id: UUID4) -> None:
    goal = await goal_crud.get_goal_by_id(session, user, goal_id)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Goal not exist",
            },
        )
    await goal_crud.delete_goal(session, goal)
