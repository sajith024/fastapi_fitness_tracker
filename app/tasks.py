import csv
from datetime import timedelta
from io import StringIO
import anyio

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings
from app.core.database import aget_db
from app.crud import users as user_crud
from app.crud import goals as goal_crud
from app.crud import workouts as workout_crud
from app.utils import date_tz, email_service

celery_app = Celery(
    "tasks", broker=str(settings.REDIS_URI), backend=str(settings.REDIS_URI)
)


celery_app.conf.beat_schedule = {
    "notify-user-fitness-goal-achieved": {
        "task": "app.tasks.notify_user_fitness_goal_achieved",
        "schedule": crontab(minute="*"),
        # "schedule": crontab(minute="0"), # every hour
    },
    "notify-user-weekly-fitness-resport": {
        "task": "app.tasks.notify_user_weekly_fitness_resport",
        "schedule": crontab(minute="*"),
        # "schedule": crontab(hour="0", minute="0", day_of_week="0"), # every week
    },
}


async def anotify_user_fitness_goal_achieved():
    async for session in aget_db():
        users = await user_crud.get_all_user(session)
        for user in users:
            goals = await goal_crud.get_achieved_goals(session, user)
            if len(goals) > 0:
                html = "<h2>Fitness Goal Achieved</h2><ul>"
                for goal in goals:
                    html += f"<li>{goal.target_exercise}: {goal.target_calories}</li>"
                html += "</ul>"

                email_service.send_email(user.email, "Fitness Goal Achieved !!!", html)
                for goal in goals:
                    goal.is_notified = True

                session.add_all(goals)
                await session.commit()


async def anotify_user_weekly_fitness_resport():
    today = date_tz.now()
    if today.weekday() == 6:
        start_date = date_tz.now() - timedelta(days=7)
        async for session in aget_db():
            users = await user_crud.get_all_user(session)
            for user in users:
                workouts = await workout_crud.weekly_fitness_trend(
                    session, user, start_date, today
                )

                if len(workouts) > 0:
                    html = "<h2>Fitness Weekly Report</h2><p>We have prepared weekly report for you.</p>"
                    buffer = StringIO()
                    writer = csv.writer(buffer)
                    header_vals = ["Date", "Calories", "Duration"]
                    writer.writerow(header_vals)
                    for workout in workouts:
                        writer.writerow(
                            [
                                workout.created_at.date(),
                                workout.calories_burned,
                                workout.duration,
                            ]
                        )
                    email_service.send_email(
                        user.email, "Fitness Weekly Report !!!", html, buffer
                    )
                else:
                    html = "<h2>Fitness Weekly Report</h2><p>You haven't done any workout this week./p>"
                    email_service.send_email(
                        user.email, "Fitness Weekly Report !!!", html
                    )


@celery_app.task()
def notify_user_fitness_goal_achieved():
    anyio.run(anotify_user_fitness_goal_achieved)


@celery_app.task()
def notify_user_weekly_fitness_resport():
    anyio.run(anotify_user_weekly_fitness_resport)
