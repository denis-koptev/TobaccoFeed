import bcrypt
from auth_page import crypto
from auth_page.models import User, Session
from django.db import IntegrityError
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect

# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# BCRYPT
# https://pypi.python.org/pypi/bcrypt/3.1.0

# SESSION KEY
# http://stackoverflow.com/questions/817882/unique-session-id-in-python

# DB_TABLES
# https://vk.com/doc21820152_445178578?hash=7f6eb8901cf9e1b18b&dl=4a50dec0735761ecff

# --------------
# auth functions
# --------------

def xprint(msg):
	print('[+] ' + str(msg))

def authentication(ident, password):

	users = User.objects.filter(Q(login=ident) | Q(mail=ident))

	if len(users) == 0:
		return None
	# user found
	# 	need to check password

	if crypto.checkpw(password, users[0].password):
		# pass is correct
		# 	need to create session key
		return users[0]
	else:
		# passwd is incorrect
		#	show error to user
		return None


def authorization(user):

	i = 5
	while i > 0:
		try:
			token = crypto.gentoken()
			session = Session(user=user, token=token)
			session.save()
		except IntegrityError as ex:
			# prevent token unique constraint error
			i -= 1
		else:
			break

	return session


def send_confirmation_mail(mail, token):

	FROM = settings.MAIL
	TO = mail

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "TobaccoFeed: confirm your account"
	msg['From'] = FROM
	msg['To'] = TO

	# Create the body of the message (a plain-text and an HTML version).
	text = "TobaccoFeed Confirmation!\nClick the link to confirm your account\nhttp://{}/auth/validate/{}".format(settings.DOMAIN, token)
	html = """\
	<html>
	  <head></head>
	  <body>
	    <center>
		    <h2>TobaccoFeed Confirmation</h2>
		    <h1>Click the link to confirm your account</h1>
	    </center>
	    <p style="text-align:center;">
		    <a href="http://{}/auth/validate/{}">
		    	<img width="50%" src="https://pp.userapi.com/c636520/v636520898/6294d/szRSNDhhjYA.jpg" />
		    </a>
	    </p>
	  </body>
	</html>
	""".format(settings.DOMAIN, token)
	print(text)
	print(html)

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP('smtp.gmail.com', 587)


	# s.ehlo()
	s.starttls()

	#Next, log in to the server
	s.login(FROM, settings.MAIL_PASS)

	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(FROM, TO, msg.as_string())
	s.quit()

def getAuthorized(request):
	usr_id = request.COOKIES.get('tfuserid')
	usr_token = request.COOKIES.get('tfsession')

	login = None

	try:
		session = Session.objects.get(user=usr_id, token=usr_token)
	except Session.DoesNotExist:
		session = None
	else:
		try:
			login = User.objects.get(id=usr_id)
		except User.DoesNotExist:
			login = None

	return login

def unauthorize(request):
		req_id = request.COOKIES.get('tfuserid')
		req_session = request.COOKIES.get('tfsession')

		try:
			session = Session.objects.get(user=req_id, token=req_session)
		except Session.DoesNotExist:
			session = None

		response = redirect("/main")

		if session != None:
			response.delete_cookie('tfuserid')
			response.delete_cookie('tfsession')
			session.delete()

		return response