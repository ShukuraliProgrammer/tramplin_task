from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user_id = models.CharField(_("user id"), unique=True, max_length=20)
    username = models.CharField(_("username"), max_length=50, blank=False, unique=True)
    phone = models.CharField(_("phone"), max_length=20, validators=[RegexValidator(r"^\+?[1-9]\d{11}$")])
    is_active = models.BooleanField(_("is active"), default=False)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return self.username


