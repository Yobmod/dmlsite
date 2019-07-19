# from django.conf import settings
from django_q.tasks import async_task  # , result


# report generator
def create_html_report() -> str:
    html_report = "We had a great quarter!"
    return html_report


def test_hook() -> None:
    pass


# report mailer
def email_report(task) -> None:
    # if task.success:
    # Email the report
    async_task(
        "django.core.mail.send_mail",  # task2 to run
        "The report you requested",  # subject
        task.result,
        "yobmod@gmail.com",  # settings.EMAIL_HOST_USER, #from email
        "yobmod@yahoo.co.uk",  # to email
    )  # task.args[0].email) #to email
    # else:
    # 	# Tell the admins something went wrong
    # 	async_task('django.core.mail.mail_admins',
    # 		'Report generation failed',
    # 		task.result)
