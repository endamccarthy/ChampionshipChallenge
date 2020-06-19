from django.db import models
from django.utils import timezone
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import F


class Region(models.TextChoices):
  CONNACHT = 'C', _('Connacht')
  LEINSTER = 'L', _('Leinster')
  MUNSTER = 'M', _('Munster')
  ULSTER = 'U', _('Ulster')
  ALL_IRELAND = 'A', _('All-Ireland')


class Sport(models.TextChoices):
  HURLING = 'H', _('Hurling')
  FOOTBALL = 'F', _('Football')


class Round(models.TextChoices):
  FIRST = '1', _('First')
  SECOND = '2', _('Second')
  THIRD = '3', _('Third')
  FOURTH = '4', _('Fourth')
  FIFTH = '5', _('Fifth')
  SIXTH = '6', _('Sixth')
  SEVENTH = '7', _('Seventh')
  EIGHTH = '8', _('Eighth')
  NINTH = '9', _('Ninth')
  TENTH = '10', _('Tenth')
  QUARTER = 'Q', _('Quarter')
  SEMI = 'S', _('Semi')
  Final = 'F', _('Final')

# def get_sentinel_user():
#   return get_user_model().objects.get_or_create(username='deleted')[0]


class Entry(models.Model):
  # user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
  points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
  date_posted = models.DateTimeField(default=timezone.now)

  # def __str__(self):
  #   return self.user.get_username()


class Team(models.Model):
  name = models.CharField(max_length=100, null=False, blank=False, unique=True)
  region = models.CharField(max_length=100, null=False, blank=False, choices=Region.choices)

  def __str__(self):
    return f'{self.name}'


class Player(models.Model):
  first_name = models.CharField(max_length=100, null=False, blank=False)
  last_name = models.CharField(max_length=100, null=False, blank=False)
  team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='team')
  sport = models.CharField(max_length=100, null=False, blank=False, choices=Sport.choices)

  def __str__(self):
    return f'{self.get_sport_display()}, {self.team}, {self.first_name} {self.last_name}'


class Fixture(models.Model):
  team_A = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='team_A')
  team_B = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='team_B')
  date = models.DateTimeField(null=True, blank=True)
  sport = models.CharField(max_length=100, null=False, blank=False, choices=Sport.choices)
  region = models.CharField(max_length=100, null=False, blank=False, choices=Region.choices)
  fixture_round = models.CharField(max_length=100, null=False, blank=False, choices=Round.choices)
  location = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='location')

  def clean(self):
    if self.team_A == self.team_B:
      raise ValidationError(_('Teams must be different'))

  def __str__(self):
    return f'{self.team_A} v {self.team_B} ({self.date.date() if self.date != None else "Date Not Set"})'


class Result(models.Model):
  fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE, null=False, blank=False, related_name='fixture')
  team_A_goals = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
  team_A_points = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
  team_B_goals = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
  team_B_points = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

  def __str__(self):
    return f'{self.fixture.date.date() if self.fixture.date != None else "Date Not Set"}, {self.fixture.team_A} {self.team_A_goals}-{self.team_A_points} : {self.team_B_goals}-{self.team_B_points} {self.fixture.team_B}'


class Score(models.Model):
  player = models.ForeignKey(Player, on_delete=models.CASCADE, null=False, blank=False, related_name='player')
  fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE, null=False, blank=False, related_name='score_fixture')
  goals_open_play = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  goals_placed_balls = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  points_open_play = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  points_placed_balls = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

  def __str__(self):
    return f'{self.player.first_name} {self.player.last_name}; {self.fixture}; {self.goals_open_play + self.goals_placed_balls}-{self.points_open_play + self.points_placed_balls}'