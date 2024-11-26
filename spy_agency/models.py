from django.db import models


class SpyCat(models.Model):
    class Breed(models.TextChoices):
        SIAMESE = "siamese"
        PERSIAN = "persian"
        MAIN_COON = "main_coon"
        RAGDOLL = "ragdoll"

    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=9, choices=Breed)
    salary = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return self.name


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
