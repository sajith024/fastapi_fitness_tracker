from io import StringIO
import logging
import emails

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_email(
    email_to: str,
    subject: str = "",
    html_content: str = "",
    attachment: StringIO | None = None,
) -> None:
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    if attachment:
        attachment.seek(0)
        message.attach(filename="report.csv", data=attachment)

    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"send email result: {response}")
