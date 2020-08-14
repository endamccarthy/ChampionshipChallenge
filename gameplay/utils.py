from django.db.models import Q
from django.shortcuts import redirect

from .models import Entry, Fixture, PredictionOption, Result, Score


def get_all_round_matches_details():
  matches = []
  fixtures = get_all_round_fixtures()

  for fixture in fixtures:
    match = {}
    match['fixture'] = fixture
    try:
      result = Result.objects.get(fixture=fixture)
      if result.final_result:
        match['result'] = result
        match['scorers'] = get_scorers_for_result(result)
    except Result.DoesNotExist:
      return redirect('gameplay_error_page')
    matches.append(match)

  return matches


def get_all_round_fixtures():
  return Fixture.objects.all().exclude(Q(fixture_round='F')).order_by('fixture_round')


def get_all_round_fixtures_not_played():
  fixtures = []
  results = Result.objects.filter(final_result=False)
  for result in results:
    fixtures.append(result.fixture)
  return fixtures


def get_scorers_for_result(result):
  scorers = Score.objects.filter(
      fixture=result.fixture).order_by('-total_score_value')
  return scorers


def get_single_instance(Model, instance_id):
  try:
    instance = Model.objects.get(id=instance_id)
    return instance
  except Model.DoesNotExist:
    return redirect('gameplay_error_page')


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


def update_all_positions():
  entries = get_all_entries().order_by('-points')
  for i in range(len(entries) - 1):
    if entries[i].points == entries[i + 1].points:
      entries[i + 1].position = entries[i].position
    else:
      entries[i + 1].position = i + 2
    entries[i + 1].save()
