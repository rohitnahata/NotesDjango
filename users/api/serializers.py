from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    password2 = CharField(label="Confirm password")

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get("password")
        if password1 != value:
            raise ValidationError("Passwords do not match")
        return value

    # def validate(self, data):
    #     email = data['email']
    #     user_qs = User.objects.filter(email=email)
    #     if user_qs.exists:
    #         raise ValidationError("User with this email address already exists")
    #     return data

    def create(self, validated_data):
        print(validated_data)
        username = validated_data["username"]
        password = validated_data["password"]
        user_obj = User(
            username=username
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "token",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        user_obj = None
        username = data["username"]
        password = data["password"]
        user = User.objects.filter(username=username)
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username is not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Invalid Credentials")
        data["token"] = "SOME TOKEN"
        return data


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]
