from django.core.mail import send_mail
from MarketPlace.celery import app

@app.task
def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/user/activate/{activation_code}/'
    message = f'Thank you for signing.Activation link: {activation_url}'

    send_mail('Activate your account', message, 'example@test.com', [email,], fail_silently=False)
