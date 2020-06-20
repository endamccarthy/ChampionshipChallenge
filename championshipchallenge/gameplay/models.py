from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import F
from users.models import CustomUser


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


class Prediction(models.TextChoices):
  TEAM_A_WIN = 'A', _('Team A Win')
  TEAM_B_WIN = 'B', _('Team B Win')
  DRAW = 'D', _('Draw')


def get_sentinel_user():
  return get_user_model().objects.get_or_create(username='deleted')[0]


class Team(models.Model):
  name = models.CharField(max_length=100, null=False, blank=False, unique=True)
  region = models.CharField(max_length=100, null=False, blank=False, choices=Region.choices)

  def __str__(self):
    return f'{self.name}'


class Player(models.Model):
  first_name = models.CharField(max_length=100, null=False, blank=False)
  last_name = models.CharField(max_length=100, null=False, blank=False)
  team = models.ForeignKey(Team, on_delete=models.PROTECT, null=False, blank=False, related_name='team')
  sport = models.CharField(max_length=100, null=False, blank=False, choices=Sport.choices)

  def __str__(self):
    return f'{self.get_sport_display()}, {self.team}, {self.first_name} {self.last_name}'


class Fixture(models.Model):
  team_A = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True, related_name='team_A')
  team_B = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True, related_name='team_B')
  date = models.DateTimeField(null=True, blank=True)
  sport = models.CharField(max_length=100, null=False, blank=False, choices=Sport.choices)
  region = models.CharField(max_length=100, null=False, blank=False, choices=Region.choices)
  fixture_round = models.CharField(max_length=100, null=False, blank=False, choices=Round.choices)
  location = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True, related_name='location')

  def clean(self):
    if (self.team_A != None and self.team_B != None) and self.team_A == self.team_B:
      raise ValidationError(_('Teams must be different'))

  def __str__(self):
    return f'{self.team_A} v {self.team_B} ({self.date.date() if self.date != None else "Date Not Set"})'


class Result(models.Model):
  fixture = models.ForeignKey(Fixture, on_delete=models.PROTECT, null=False, blank=False, related_name='fixture')
  team_A_goals = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
  team_A_points = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
  team_B_goals = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
  team_B_points = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

  def __str__(self):
    return f'{self.fixture.date.date() if self.fixture.date != None else "Date Not Set"}, {self.fixture.team_A} {self.team_A_goals}-{self.team_A_points} : {self.team_B_goals}-{self.team_B_points} {self.fixture.team_B}'


class Score(models.Model):
  player = models.ForeignKey(Player, on_delete=models.PROTECT, null=False, blank=False, related_name='player')
  fixture = models.ForeignKey(Fixture, on_delete=models.PROTECT, null=False, blank=False, related_name='score_fixture')
  goals_open_play = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  goals_placed_balls = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  points_open_play = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  points_placed_balls = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

  def __str__(self):
    return f'{self.player.first_name} {self.player.last_name}; {self.fixture}; {self.goals_open_play + self.goals_placed_balls}-{self.points_open_play + self.points_placed_balls}'


class Prediction(models.Model):
  fixture = models.ForeignKey(Fixture, on_delete=models.PROTECT, null=False, blank=False, related_name='prediction_fixture')
  prediction = models.CharField(max_length=100, null=False, blank=False, choices=Prediction.choices)

  def __str__(self):
    return f'{self.fixture}, {self.get_prediction_display()}'
    

class Participants(models.Model):
  fixture = models.ForeignKey(Fixture, on_delete=models.PROTECT, null=False, blank=False, related_name='participants_fixture')
  team_A = models.ForeignKey(Team, on_delete=models.PROTECT, null=False, blank=False, related_name='participants_team_A')
  team_B = models.ForeignKey(Team, on_delete=models.PROTECT, null=False, blank=False, related_name='participants_team_B')

  def clean(self):
    if self.team_A == self.team_B:
      raise ValidationError(_('Teams must be different'))

  def __str__(self):
    return f'{self.fixture.get_region_display()} {self.fixture.get_fixture_round_display()}: {self.team_A} - {self.team_B}'


class Entry(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.SET(get_sentinel_user), null=False, blank=False, related_name='entry_user')
  datetime = models.DateTimeField(default=timezone.now, null=False, blank=True)
  points = models.IntegerField(default=0, validators=[MinValueValidator(0)], null=False, blank=True)
  paid = models.BooleanField(default=False, null=False, blank=True)
  predictions = models.ManyToManyField(Prediction, related_name = 'entry_prediction')
  participants = models.ManyToManyField(Participants, related_name = 'entry_participants')

  def __str__(self):
    return f'{self.user.get_username()}'