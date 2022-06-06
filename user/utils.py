from django.core.mail import send_mail
from MarketPlace.celery import app

@app.task
def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/user/activate/{activation_code}/'
    message = f'Thank you for signing.Activation link: {activation_url}'

    send_mail('Activate your account', message, 'example@test.com', [email,], fail_silently=False)


def send_confirmation_email(user):
    code = user.activation_code
    full_link = f'http://localhost:8001/api/v1/account/activate/{code}/'
    to_email = user.email
    send_mail('Здравствуйте, активируйте ваш аккаунт',
              f'Чтобы активировать ваш аккаунт нужно перейти по ссылке: {full_link}',
              'from@example.com', [to_email,], fail_silently=False)


def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail('Восстановление пароля',
              f'Ваш код: {code}',
              'from@example.com',
              [to_email], fail_silently=False,)
