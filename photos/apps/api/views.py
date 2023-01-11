import datetime

from django.db.models.expressions import RawSQL
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Photo, Name
from .serializers import (
    PhotoSerializer,
    ThinPhotoSerializer,
    UserSerializer,
    NameSerializer,
)

DISTANCE_PRECISE_METERS = 100 / 1000


class PhotoViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""

        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, *args, **kwargs):
        """Returns a list of all photos uploaded by user with filters"""

        queryset = self.get_queryset()

        if date_from := self.request.query_params.get("datefrom"):
            queryset = queryset.filter(uploaded__gte=datetime.datetime.fromtimestamp(int(date_from)))
        if date_to := self.request.query_params.get("dateto"):
            queryset = queryset.filter(uploaded__lte=datetime.datetime.fromtimestamp(int(date_to)))
        if name := self.request.query_params.get("name"):
            queryset = queryset.filter(names__name=name)
        if location := self.request.query_params.get("location"):
            latitude, longitude = location.split(",")
            queryset = self.annotate_distance(queryset, latitude, longitude).filter(
                distance__lt=DISTANCE_PRECISE_METERS
            )
        if queryset:
            serializer = ThinPhotoSerializer(data=queryset, many=True)
            serializer.is_valid()
            return Response(serializer.data)
        else:
            return Response([])

    def create(self, *args, **kwargs):
        description = self.request.POST.get("description")
        file = self.request.FILES.get("photo")
        if location := self.request.POST.get("location"):
            latitude, longitude = location.split(",")
            photo = Photo.objects.create(
                owner=self.request.user,
                photo=file,
                description=description,
                latitude=latitude,
                longitude=longitude,
            )
        else:
            photo = Photo.objects.create(
                owner=self.request.user,
                photo=file,
                description=description,
            )
        names = self.request.POST.get("people").split(",")
        for name in names:
            n = Name.objects.get_or_create(name=name.strip(), owner=self.request.user)[0]
            photo.names.add(n)
        Serializer = self.get_serializer_class()
        serializer = Serializer(data=photo)
        serializer.is_valid()
        return Response(serializer.data)

    @staticmethod
    def annotate_distance(queryset, latitude, longitude):
        """Annotates queryset with a distance in kilometers,
        using the great circle distance formula.
        """
        gcd_sql = "6371 * acos(least(greatest(\
        cos(radians(%s)) * cos(radians(latitude)) \
        * cos(radians(longitude) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(latitude)) \
        , -1), 1))"
        distance_raw_sql = RawSQL(gcd_sql, (latitude, longitude, latitude))
        return queryset.annotate(distance=distance_raw_sql)


@api_view(["POST"])
def register(request):
    """Creates user profile"""
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
    else:
        return Response(status=400)

    return Response(get_tokens_for_user(user))


def get_tokens_for_user(user):
    """Returns auth token for a user"""
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["GET"])
def get_names(request):
    if name := request.GET.get("name"):
        queryset = Name.objects.filter(owner=request.user, name__contains=name)
        serializer = NameSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    else:
        return Response(status=400)
