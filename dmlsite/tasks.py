from django.conf import settings
from django_q.tasks import async, result

# report generator
def create_html_report():
	html_report = 'We had a great quarter!'
	return html_report

def test_hook(task):
	pass

# report mailer
def email_report():
	#if task.success:
		# Email the report
	async('django.core.mail.send_mail', #task2 to run
		'The report you requested', #subject
		'what what',   #task.result,
		'yobmod@gmail.com',  #settings.EMAIL_HOST_USER, #from email
		'yobmod@yahoo.co.uk') #task.args[0].email) #to email
	# else:
	# 	# Tell the admins something went wrong
	# 	async('django.core.mail.mail_admins',
	# 		'Report generation failed',
	# 		task.result)
