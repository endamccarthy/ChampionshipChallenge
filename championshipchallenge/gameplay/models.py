# from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Sport(models.TextChoices):
  HURLING = 'H', _('Hurling')
  FOOTBALL = 'F', _('Football')


class Region(models.TextChoices):
  CONNACHT = 'C', _('Connacht')
  LEINSTER = 'L', _('Leinster')
  MUNSTER = 'M', _('Munster')
  ULSTER = 'U', _('Ulster')
  ALL_IRELAND = 'A', _('All-Ireland')


class County(models.TextChoices):
  ANTRIM = 'AM', _('Antrim')
  ARMAGH = 'AH', _('Armagh')
  CARLOW = 'CW', _('Carlow')
  CAVAN = 'CN', _('Cavan')
  CLARE = 'CE', _('Clare')
  CORK = 'CK', _('Cork')
  DERRY = 'DY', _('Derry')
  DONEGAL = 'DL', _('Donegal')
  DOWN = 'DN', _('Down')
  DUBLIN = 'DB', _('Dublin')
  FERMANAGH = 'FH', _('Fermanagh')
  GALWAY = 'GY', _('Galway')
  KERRY = 'KY', _('Kerry')
  KILDARE = 'KE', _('Kildare')
  KILKENNY = 'KK', _('Kilkenny')
  LAOIS = 'LS', _('Laois')
  LEITRIM = 'LM', _('Leitrim')
  LIMERICK = 'LK', _('Limerick')
  LONDON = 'LN', _('London')
  LONGFORD = 'LD', _('Longford')
  LOUTH = 'LH', _('Louth')
  MAYO = 'MO', _('Mayo')
  MEATH = 'MH', _('Meath')
  MONAGHAN = 'MN', _('Monaghan')
  NEW_YORK = 'NY', _('New York')
  OFFALY = 'OY', _('Offaly')
  ROSCOMMON = 'RN', _('Roscommon')
  SLIGO = 'SO', _('Sligo')
  TIPPERARY = 'TY', _('Tipperary')
  TYRONE = 'TE', _('Tyrone')
  WATERFORD = 'WD', _('Waterford')
  WESTMEATH = 'WH', _('Westmeath')
  WEXFORD = 'WX', _('Wexford')
  WICKLOW = 'WW', _('Wicklow')


class Round(models.TextChoices):
  FIRST = '1', _('First Round')
  SECOND = '2', _('Second Round')
  THIRD = '3', _('Third Round')
  FOURTH = '4', _('Fourth Round')
  FIFTH = '5', _('Fifth Round')
  SIXTH = '6', _('Sixth Round')
  SEVENTH = '7', _('Seventh Round')
  EIGHTH = '8', _('Eighth Round')
  NINTH = '9', _('Ninth Round')
  TENTH = '10', _('Tenth Round')
  QUARTER = 'Q', _('Quarter Final')
  SEMI = 'S', _('Semi Final')
  FINAL = 'F', _('Final')


class PredictionOption(models.TextChoices):
  TEAM_A_WIN = 'A', _('Team A Win')
  TEAM_B_WIN = 'B', _('Team B Win')
  DRAW = 'D', _('Draw')


def get_sentinel_user():
  return get_user_model().objects.get_or_create(username='deleted')[0]


class Team(models.Model):
  name = models.CharField(max_length=100, null=False,
                          blank=False, choices=County.choices, unique=False)
  region = models.CharField(max_length=100, null=False,
                            blank=False, choices=Region.choices)
  sport = models.CharField(max_length=100, null=False,
                           blank=False, choices=Sport.choices)

  class Meta:
    constraints = [
        models.UniqueConstraint(fields=['name', 'sport'], name='unique team')
    ]

  def __str__(self):
    return f'{self.get_name_display()} {self.get_sport_display()}'


class Player(models.Model):
  first_name = models.CharField(max_length=100, null=False, blank=False)
  last_name = models.CharField(max_length=100, null=False, blank=False)
  team = models.ForeignKey(Team, on_delete=models.PROTECT,
                           null=False, blank=False, related_name='team')
  active = models.BooleanField(default=True, null=False, blank=False)

  class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['first_name', 'last_name', 'team'], name='unique player')
    ]

  def __str__(self):
    return f'{self.first_name} {self.last_name} - {self.team}'


class Fixture(models.Model):
  team_A = models.ForeignKey(
      Team, on_delete=models.PROTECT, null=True, blank=True, related_name='team_A')
  team_B = models.ForeignKey(
      Team, on_delete=models.PROTECT, null=True, blank=True, related_name='team_B')
  datetime = models.DateTimeField(null=False, blank=False)
  sport = models.CharField(max_length=100, null=False,
                           blank=False, choices=Sport.choices)
  region = models.CharField(max_length=100, null=False,
                            blank=False, choices=Region.choices)
  fixture_round = models.CharField(
      max_length=100, null=False, blank=False, choices=Round.choices)
  location = models.CharField(
      max_length=100, null=True, blank=True, choices=County.choices)

  class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['team_A', 'team_B', 'datetime'], name='unique fixture')
    ]

  def clean(self):
    if (self.fixture_round in ['Q', 'S', 'F']):
      fixture_filter_1 = Fixture.objects.filter(
          sport=self.sport,
          region=self.region,
          fixture_round=self.fixture_round,
          datetime__year=self.datetime.date().year
      ).exclude(pk=self.pk)
      if fixture_filter_1.count() >= 1:
        raise ValidationError(
            _('This knock out fixture has already been created'))
    else:
      if (self.team_A is None or self.team_B is None):
        raise ValidationError(_('Teams are required for round fixtures'))
      fixture_filter_2 = Fixture.objects.filter(
          Q(team_A=self.team_A) | Q(team_A=self.team_B) | Q(
              team_B=self.team_B) | Q(team_B=self.team_A),
          sport=self.sport,
          region=self.region,
          fixture_round=self.fixture_round,
          datetime__year=self.datetime.date().year
      ).exclude(pk=self.pk)
      if fixture_filter_2.count() >= 1:
        raise ValidationError(
            _('One or both of these teams already has an entry for this round'))
    if (self.team_A is not None and self.team_B is not None):
      if self.team_A == self.team_B:
        raise ValidationError(_('Teams must be different'))
      if (self.team_A.region != self.region and self.region != 'A'):
        raise ValidationError(_(f'Wrong Region for {self.team_A}'))
      if (self.team_B.region != self.region and self.region != 'A'):
        raise ValidationError(_(f'Wrong Region for {self.team_B}'))

  def __str__(self):
    return_string = f'{self.datetime.date().year} - {self.get_region_display()} {self.get_sport_display()} {self.get_fixture_round_display()}'
    if self.team_A is not None and self.team_B is not None:
      return_string += f' - {self.team_A} v {self.team_B}'
    return return_string


class Result(models.Model):
  fixture = models.OneToOneField(
      Fixture, on_delete=models.PROTECT, null=False, blank=False, related_name='fixture')
  team_A_goals = models.IntegerField(default=0, null=True, blank=True, validators=[
      MinValueValidator(0), MaxValueValidator(100)])
  team_A_points = models.IntegerField(default=0, null=True, blank=True, validators=[
      MinValueValidator(0), MaxValueValidator(100)])
  team_B_goals = models.IntegerField(default=0, null=True, blank=True, validators=[
      MinValueValidator(0), MaxValueValidator(100)])
  team_B_points = models.IntegerField(default=0, null=True, blank=True, validators=[
      MinValueValidator(0), MaxValueValidator(100)])
  final_result = models.BooleanField(default=False, null=False, blank=False)

  def __str__(self):
    return_string = f'{self.fixture}'
    if (self.fixture.team_A is not None and self.fixture.team_B is not None):
      return_string += f' - {self.team_A_goals}-{self.team_A_points} : {self.team_B_goals}-{self.team_B_points}'
    return return_string


class Score(models.Model):
  player = models.ForeignKey(
      Player, on_delete=models.PROTECT, null=False, blank=False, related_name='player')
  fixture = models.ForeignKey(Fixture, on_delete=models.PROTECT,
                              null=False, blank=False, related_name='score_fixture')
  goals_open_play = models.IntegerField(
      default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  goals_placed_balls = models.IntegerField(
      default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  points_open_play = models.IntegerField(
      default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  points_placed_balls = models.IntegerField(
      default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

  class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['player', 'fixture'], name='unique score')
    ]

  def clean(self):
    if self.fixture.datetime >= timezone.now():
      raise ValidationError(
          _('Match has not taken place yet, try changing details in fixtures'))
    if (self.player.team != self.fixture.team_A and self.player.team != self.fixture.team_B):
      raise ValidationError(
          _('This player does not play with either of the teams involved'))
    try:
      if Result.objects.get(fixture=self.fixture).final_result:
        raise ValidationError(
            _('The result for this game has been marked as final, please change this in results to add or change a score'))
    except Result.DoesNotExist:
      raise ValidationError(
          _('The result for this fixture does not exist, try creating a new result first'))

  def __str__(self):
    return f'{self.fixture} - {self.player.first_name} {self.player.last_name}'


class Prediction(models.Model):
  fixture = models.ForeignKey(Fixture, on_delete=models.PROTECT,
                              null=False, blank=False, related_name='prediction_fixture')
  prediction = models.CharField(
      max_length=100, null=True, blank=False, choices=PredictionOption.choices)

  class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['fixture', 'prediction'], name='unique prediction')
    ]

  def __str__(self):
    return f'{self.fixture}, {self.get_prediction_display()}'


class Finalist(models.Model):
  fixture = models.ForeignKey(Fixture, on_delete=models.PROTECT,
                              null=False, blank=False, related_name='finalist_fixture')
  team_A = models.ForeignKey(Team, on_delete=models.PROTECT,
                             null=False, blank=False, related_name='finalist_team_A')
  team_B = models.ForeignKey(Team, on_delete=models.PROTECT,
                             null=False, blank=False, related_name='finalist_team_B')

  def clean(self):
    if (self.fixture.fixture_round not in ['Q', 'S', 'F']):
      raise ValidationError(
          _('Finalists prediction only available for knock-out stages'))
    if self.team_A == self.team_B:
      raise ValidationError(_('Teams must be different'))
    if (self.team_A.region != self.fixture.region and self.fixture.region != 'A'):
      raise ValidationError(_(f'Wrong Region for {self.team_A}'))
    if (self.team_B.region != self.fixture.region and self.fixture.region != 'A'):
      raise ValidationError(_(f'Wrong Region for {self.team_B}'))
    if (self.team_A.sport != self.fixture.sport and self.fixture.sport != 'A'):
      raise ValidationError(_(f'Wrong Sport for {self.team_A}'))
    if (self.team_B.sport != self.fixture.sport and self.fixture.sport != 'A'):
      raise ValidationError(_(f'Wrong Sport for {self.team_B}'))

  def __str__(self):
    return f'{self.fixture} - {self.team_A} v {self.team_B}'


class TopScorer(models.Model):
  region = models.CharField(max_length=100, null=False,
                            blank=False, choices=Region.choices)
  sport = models.CharField(max_length=100, null=False,
                           blank=False, choices=Sport.choices)
  player = models.ForeignKey(Player, on_delete=models.PROTECT,
                             null=False, blank=False, related_name='top_scorer')
  goals = models.IntegerField(
      default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
  points = models.IntegerField(
      default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])

  def clean(self):
    if self.region != self.player.team.region:
      raise ValidationError(_('Player is not in this region'))
    if self.sport != self.player.team.sport:
      raise ValidationError(_('Player does not play this sport'))

  def __str__(self):
    return f'{self.player} - {self.goals}-{self.points}'


class Entry(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.SET(
      get_sentinel_user), null=False, blank=False, related_name='entry_user')
  datetime = models.DateTimeField(default=timezone.now, null=False, blank=True)
  points = models.IntegerField(
      default=0, validators=[MinValueValidator(0)], null=False, blank=True)
  paid = models.BooleanField(default=False, null=False, blank=True)
  predictions = models.ManyToManyField(
      Prediction, related_name='entry_predictions')
  # finalists = models.ManyToManyField(Finalist, related_name = 'entry_finalists')
  # top_scorers = models.ManyToManyField(TopScorer, related_name = 'entry_top_scorers')
  position = models.IntegerField(
      default=1, validators=[MinValueValidator(1)], null=False, blank=True)
  entry_number = models.IntegerField(
      default=1, validators=[MinValueValidator(1)], null=False, blank=True)

  class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['user', 'datetime'], name='unique entry')
    ]

  def get_total_number_of_entries(self):
    return Entry.objects.all().count()

  def get_number_of_entries_by_user(self):
    return Entry.objects.filter(user=self.user).count()

  def get_number_of_tied_entries(self):
    return Entry.objects.filter(position=self.position).count()

  def save(self, *args, **kwargs):  # pylint: disable=signature-differs
    # if the entry is new (not being edited)
    if self.pk is None:
      count = self.get_number_of_entries_by_user()
      if count >= 1:
        self.entry_number = count + 1
    super(Entry, self).save(*args, **kwargs)

  def __str__(self):
    return_string = f'{self.datetime.date().year} - {self.user.first_name} {self.user.last_name}'
    if self.entry_number > 1:
      return_string += f' ({self.entry_number})'
    return return_string
