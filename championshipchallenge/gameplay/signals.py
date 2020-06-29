from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Fixture, Result, Score, Entry, PredictionOption
from django.db.models import F


@receiver(post_save, sender=Fixture)
def create_result(sender, instance, created, **kwargs):
  if created:
    Result.objects.create(fixture=instance)


@receiver(post_save, sender=Score)
def update_result(sender, instance, **kwargs):
  try:
    result = Result.objects.get(fixture=instance.fixture)
  except Result.DoesNotExist:
    result = None
  
  if result is not None:
    scores = Score.objects.filter(fixture=instance.fixture).all()
    team_A_goals = 0
    team_A_points = 0
    team_B_goals = 0
    team_B_points = 0
    
    for score in scores:
      if score.player.team == score.fixture.team_A:
        team_A_goals += score.goals_open_play + score.goals_placed_balls
        team_A_points += score.points_open_play + score.points_placed_balls
      elif score.player.team == score.fixture.team_B:
        team_B_goals += score.goals_open_play + score.goals_placed_balls
        team_B_points += score.points_open_play + score.points_placed_balls

      result.team_A_goals = team_A_goals
      result.team_A_points = team_A_points
      result.team_B_goals = team_B_goals
      result.team_B_points = team_B_points

    result.save()


@receiver(post_save, sender=Result)
def finalize_result(sender, instance, created, **kwargs):
  update_all_points()


def update_all_points():
  entries = get_all_entries()
  results = get_all_final_results()
  for entry in entries:
    entry.points = 0
    for result in results:
      outcome = determine_match_outcome(result)
      update_points_per_entry_per_result(entry, result, outcome)


def get_all_entries():
  return Entry.objects.all()


def get_all_final_results():
  return Result.objects.filter(final_result=True)


def determine_match_outcome(result):
  team_A_score = (result.team_A_goals * 3) + (result.team_A_points)
  team_B_score = (result.team_B_goals * 3) + (result.team_B_points)
  if team_A_score > team_B_score:
    return PredictionOption.TEAM_A_WIN
  elif team_B_score > team_A_score:
    return PredictionOption.TEAM_B_WIN
  else:
    return PredictionOption.DRAW


def update_points_per_entry_per_result(entry, result, outcome):
  for prediction in entry.predictions.all():
    if prediction.fixture == result.fixture:
      if prediction.prediction == outcome:
        if prediction.prediction == PredictionOption.DRAW:
          entry.points += 10
        else:
          entry.points += 5
        entry.save()