from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_mail(MSG,user,subjectMSG,Text,email):
    subject = subjectMSG
                
    context = {'user':user,'Otp':MSG,'Text':Text}
    html_content = render_to_string("send_Mail.html",context)
    text_content = strip_tags(html_content)
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]

    email = EmailMultiAlternatives(subject,text_content, email_from, recipient_list)
    email.attach_alternative(html_content,"text/html")
    email.send()