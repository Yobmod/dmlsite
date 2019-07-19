# from django.conf import settings
from django_q.tasks import async_task  # , result


def create_html_report() -> str:
    html_report = "We had a great quarter!"
    return html_report


# report mailer
def email_report(subject: str, text: str, to_email: str, from_email: str = "yobmod@gmail.com") -> None:
    """Add report to task queue for async emailing"""
    # if task.success:   # Email the report
    async_task(
        "django.core.mail.send_mail",  # task2 to run
        subject,  # subject
        text,  # task.result,
        from_email,  # settings.EMAIL_HOST_USER, #from email
        to_email,  # to email
    )  # task.args[0].email)
    # else:
    # 	# Tell the admins something went wrong
    # 	async_task('django.core.mail.mail_admins',
    # 		'Report generation failed',
    # 		task.result)
