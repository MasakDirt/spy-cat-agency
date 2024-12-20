from django.core.exceptions import ValidationError
from django.db import models

from spy_agency.validators import validate_cat_breed


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        validate_cat_breed(self.breed, ValidationError)

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class Mission(models.Model):
    is_complete = models.BooleanField(default=False)
    cat = models.OneToOneField(
        SpyCat,
        on_delete=models.SET_NULL,
        related_name="mission",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"Mission for '{self.cat.name}' with id - {self.id}"


class Target(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name="targets"
    )

    def __str__(self) -> str:
        return self.name
