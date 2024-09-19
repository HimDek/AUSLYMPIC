import os
import datetime
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def sport_image_path(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"sport_{instance.id}_{instance.name}_image{ext}"


def sport_fixture_path(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"sport_{instance.id}_{instance.name}_fixture{ext}"


def sport_rulebook_path(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"sport_{instance.id}_{instance.name}_rulebook{ext}"


def notice_file_path(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"notice_{instance.id}_{base}{ext}"


def get_first_name(self):
    return f"{self.first_name} {self.last_name}"


User.add_to_class("__str__", get_first_name)


class Department(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    @property
    def get_name(self):
        return self.name.replace("Department of", "")

    @property
    def gold_winners(self):
        return Team.objects.filter(department=self, gold_winner=True)

    @property
    def silver_winners(self):
        return Team.objects.filter(department=self, silver_winner=True)

    @property
    def bronze_winners(self):
        return Team.objects.filter(department=self, bronze_winner=True)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to=sport_image_path, blank=True, null=False, default="/static/banner.jpg"
    )
    coordinators = models.ManyToManyField(User, blank=True, related_name="sport")

    team_size_min = models.PositiveIntegerField(default=1, blank=False, null=False)
    team_size_max = models.PositiveIntegerField(default=1, blank=False, null=False)

    department_limit = models.PositiveIntegerField(blank=True, null=True, help_text="Limit the number of Teams from one Department")

    fixtures = models.FileField(upload_to=sport_fixture_path, blank=True, null=True)
    rulebook = models.FileField(upload_to=sport_rulebook_path, blank=True, null=True)

    registration_deadline = models.DateTimeField(blank=False, null=False, default=timezone.datetime(2024, 9, 18, 8, 30, 0, 0, tzinfo=datetime.timezone.utc))

    @property
    def winners(self):
        return Team.objects.filter(Q(sport=self) & Q(Q(gold_winner=True) | Q(silver_winner=True) | Q(bronze_winner=True)))

    @property
    def loosers(self):
        return Team.objects.filter(Q(sport=self) & Q(gold_winner=False) & Q(silver_winner=False) & Q(bronze_winner=False))

    @property
    def gold_winners(self):
        return Team.objects.filter(sport=self, gold_winner=True)

    @property
    def silver_winners(self):
        return Team.objects.filter(sport=self, silver_winner=True)

    @property
    def bronze_winners(self):
        return Team.objects.filter(sport=self, bronze_winner=True)

    def __str__(self):
        return self.name

    def clean(self):
        # Validate that team_size_max is greater than or equal to team_size_min
        if self.team_size_max < self.team_size_min:
            raise ValidationError(
                {
                    "team_size_max": "Maximum team size cannot be less than the minimum team size."
                }
            )

    def save(self, *args, **kwargs):
        # Call clean method before saving the instance
        self.clean()
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['id']


class Team(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    phone = models.PositiveBigIntegerField(validators=[MinValueValidator(6000000000), MaxValueValidator(9999999999)], blank=False, null=False, help_text="Participant/Captain's Phone number")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="teams",
    )
    sport = models.ForeignKey(
        Sport, on_delete=models.CASCADE, null=False, blank=False, related_name="teams"
    )
    members = models.JSONField(blank=True, null=True)
    gold_winner = models.BooleanField(default=False)
    silver_winner = models.BooleanField(default=False)
    bronze_winner = models.BooleanField(default=False)
    winning_sub_category = models.CharField(max_length=31, blank=True, null=False, default="")

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['sport'],
    #             name='unique_winner_per_sport',
    #             condition=models.Q(winner=True)
    #         )
    #     ]

    def save(self, *args, **kwargs):
        if self.sport.department_limit:
            current_count = Team.objects.filter(sport=self.sport, department=self.department).count()
            if self.pk is None and current_count >= self.sport.department_limit:
                raise ValidationError(f'Cannot have more than {self.sport.department_limit} teams for {self.sport} from {self.department}.')
        super().save(*args, **kwargs)

    @property
    def members_display(self):
        return ", ".join(self.members)

    def __str__(self):
        return f"{self.name} {self.department}"


    class Meta:
        ordering = ['-gold_winner', '-silver_winner', '-bronze_winner', 'winning_sub_category', 'department', 'id']


class Notice(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    file = models.FileField(upload_to=notice_file_path, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        ordering = ["-modified", "-added"]

class SportGroup(models.Model):
    name = models.CharField(max_length=100)
    sub = models.CharField(max_length=100, blank=True)
    sports = models.ManyToManyField(Sport, related_name="group")

    class Meta:
        unique_together = [["name", "sub"]]

    def __str__(self):
        return self.name


    class Meta:
        ordering = ["id"]