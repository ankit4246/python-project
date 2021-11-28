from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStamp(models.Model):
    """General Abstract model that can inherited by other model which requires timestamp"""

    created_at = models.DateTimeField(
        _("Created Date"),
        auto_now_add=True,
        help_text=_("Eg. 2021-09-28T19:40:02.785988+05:45"),
    )
    updated_at = models.DateTimeField(
        _("Updated Date"),
        auto_now=True,
        help_text=_("Eg. 2021-09-28T19:40:02.785988+05:45"),
    )

    class Meta:
        abstract = True


class Menu(TimeStamp):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    order_id = models.PositiveSmallIntegerField(null=True, blank=True)
    url = models.CharField(max_length=100)
    ic_class = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name} (CODE:{self.code})"

    class Meta:
        ordering = ["order_id"]

    @property
    def has_child(self):
        return self.children.all().exists()

    def save(self, *args, **kwargs):
        if not self.order_id:
            try:
                self.order_id = Menu.objects.order_by("pk").last().order_id + 1
            except Exception as e:
                self.order_id = 1
        return super().save(*args, **kwargs)


class MenuPermission(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="permissions")
    role = models.ForeignKey(
        "Role",
        blank=True,
        related_name="menu_permissions",
        null=True,
        on_delete=models.CASCADE,
    )
    can_add = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role} ==> {self.menu}"


class Role(TimeStamp):
    name = models.CharField(max_length=50, unique=True)
    desc = models.TextField(_("Description"), blank=True, null=True)
    menus = models.ManyToManyField(Menu, blank=True)

    def __str__(self):
        return self.name

    @property
    def total_users(self):
        return self.users.count()
