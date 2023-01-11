from django.contrib.auth import get_user_model
from rest_framework.fields import CharField, DecimalField
from rest_framework.serializers import ModelSerializer
from .models import Photo, Name


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("owner", )


class ThinPhotoSerializer(PhotoSerializer):
    class Meta:
        model = Photo
        fields = ("id", "photo")


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "password")

    password = CharField(write_only=True)


class NameSerializer(ModelSerializer):
    class Meta:
        model = Name
        fields = ("name",)
