from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Fixture, Result, Score
from django.db.models import F


@receiver(post_save, sender=Fixture)
def create_result(sender, instance, created, **kwargs):
  if created:
    Result.objects.create(fixture=instance)


@receiver(post_save, sender=Score)
def update_result(sender, instance, **kwargs):
  result = Result.objects.filter(fixture=instance.fixture).first()
  if result:
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
