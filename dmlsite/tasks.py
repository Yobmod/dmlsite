from django.conf import settings
from django_q.tasks import async

# report generator
def create_html_report(user):
	html_report = 'We had a great quarter!'
	return html_report

def test_hook(task):
	pass
	
# report mailer
def email_report(task):
	if task.success:
		# Email the report
		async('django.core.mail.send_mail',
			'The report you requested',
			task.result,
			settings.EMAIL_HOST_USER,
			task.args[0].email)
	else:
		# Tell the admins something went wrong
		async('django.core.mail.mail_admins',
			'Report generation failed',
			task.result)
