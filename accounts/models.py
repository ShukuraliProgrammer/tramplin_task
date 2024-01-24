from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Profile(models.Model):
    username = models.CharField(_("username"), max_length=50, blank=False, unique=True)
    phone = models.CharField(_("phone"), max_length=20, validators=[RegexValidator(r"^\+?[1-9]\d{11}$")])

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return self.username

