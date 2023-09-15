# utils.py or any other suitable file

from django.core.mail import send_mail

def send_test_email():
    subject = 'Hello, Django Email'
    message = 'This is a test email sent from Django.'
    from_email = 'info@power-up.lu'
    recipient_list = ['tom.scheuer1993@hotmail.com']
    
    send_mail(subject, message, from_email, recipient_list)
