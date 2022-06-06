from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import MyUser
from user.utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise  serializers.ValidationError('Passwords do not match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user



class LoginSerializer (serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(label='Password', style={'input_type':'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),email=email, password=password)

            if not user:
                message = 'Unable to login'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Include email and password'
            raise serializers.ValidationError(message, code='authorization')
        attrs['user'] = user
        return attrs

User = get_user_model()

class CreateNewPasswordSerializer (serializers.Serializer):
    email = serializers.EmailField(max_length=30, required=True)
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=4, required=True)
    password2 = serializers.CharField(min_length=4, required=True)

# l = [1,2,3]
# l[1]

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password!= password2:
            raise serializers.ValidationError('Passwords do not match')
        email = attrs['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exists')

        code = attrs['code']
        if user.activation_code != code:
            raise serializers.ValidationError('Code is incorrect')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']

        user.set_password(data['password'])
        user.activation_code = ''
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30, required=True)


