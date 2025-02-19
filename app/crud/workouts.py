from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func, select

from app.models.users import User
from app.models.workouts import Workout
from app.schemas.workouts import WorkoutCreate, WorkoutUpdate


async def get_all_workouts(
    session: AsyncSession, user: User, page: int, limit: int, exercise: str
) -> list[Workout]:
    page_limit = limit * page
    offset = (page - 1) * limit
    query = (
        select(Workout)
        .options(selectinload(Workout.goal))
        .where(Workout.user == user, Workout.is_deleted == False)
    )

    if exercise:
        query = query.where(Workout.exercise == exercise)

    query = query.offset(offset).limit(page_limit)

    db_objs = await session.scalars(query)
    return list(db_objs.all())


async def total_workouts(session: AsyncSession, user: User) -> int:
    stmt = select(func.count(Workout.id)).where(
        Workout.user == user, Workout.is_deleted == False
    )
    return await session.scalar(stmt) or 0


async def get_workout(
    session: AsyncSession, user: User, workout_id: UUID
) -> Workout | None:
    query = (
        select(Workout)
        .options(selectinload(Workout.goal))
        .where(
            Workout.id == workout_id, Workout.user == user, Workout.is_deleted == False
        )
    )

    workout = await session.scalar(query)
    return workout


async def create_workout(
    session: AsyncSession, user: User, workout_data: WorkoutCreate
) -> Workout:
    workout = Workout(
        exercise=workout_data.exercise,
        duration=workout_data.duration,
        calories_burned=workout_data.calories_burned,
        user=user,
        goal_id=workout_data.goal_id,
    )

    session.add(workout)
    await session.commit()
    await session.refresh(workout)
    return workout


async def update_workout(
    session: AsyncSession, workout: Workout, workout_data: WorkoutUpdate
) -> Workout:
    workout_dump = workout_data.model_dump(exclude_unset=True)

    for var, value in workout_dump.items():
        setattr(workout, var, value)

    session.add(workout)
    await session.commit()
    await session.refresh(workout)
    return workout


async def delete_workout(session: AsyncSession, workout: Workout) -> None:
    workout.is_deleted = True
    session.add(workout)
    await session.commit()


async def weekly_fitness_trend(
    session: AsyncSession, user: User, start_date: datetime, end_date: datetime
) -> list[Workout]:
    query = (
        select(Workout)
        .where(Workout.user == user, Workout.is_deleted == False)
        .where(Workout.created_at >= start_date, Workout.created_at <= end_date)
    )
    workouts = await session.scalars(query)
    return list(workouts.all())
