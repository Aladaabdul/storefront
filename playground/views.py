from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage, mail_admins, BadHeaderError
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers

def say_hello(request):
    # try:
        # send_mail('subject', 'message', 'info@aladabuy', ['john@aladabuy'])
        # mail_admins('subject', 'message', html_message='message')
        # message = EmailMessage('subject', 'message', 
        #                        'admin@aladabuy.com', ['john@moshbuy.com'])
        # message.attach_file('playground/static/images/butterfly.jpg')
        # message.send()
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Alada'}
    #     )
    #     message.send(['Abdul@aladabuy.com'])
    # except BadHeaderError: 
    #     pass
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Alada'})
