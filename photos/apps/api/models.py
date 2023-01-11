from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from core.settings import MEDIA_ROOT

User = get_user_model()


class Name(models.Model):
    """Names of people on the photos"""

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        verbose_name=_("Who added"),
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=["name", "owner"],
                name="unique_name_for_user",
            ),
        )
        verbose_name = _("Name")
        verbose_name_plural = _("Names")


class Photo(models.Model):
    """Stores photo info"""

    owner = models.ForeignKey(
        verbose_name=_("Owner profile"),
        to=User,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(_("Photo"), upload_to=MEDIA_ROOT.joinpath("photos"))
    description = models.TextField(_("Description"), blank=True)
    latitude = models.DecimalField(_("Latitude"), decimal_places=7, max_digits=9, default=Decimal("0.0"))
    longitude = models.DecimalField(_("Longitude"), decimal_places=7, max_digits=9, default=Decimal("0.0"))
    uploaded = models.DateTimeField(_("Upload date"), auto_now_add=True)
    names = models.ManyToManyField(Name, "photos", verbose_name=_("People on the photo"))

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")
