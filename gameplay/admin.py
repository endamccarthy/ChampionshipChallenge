from django.contrib import admin

from .models import (Entry, Finalist, Fixture, Player, Prediction, Result,
                     Score, Team, TopScorer)

# class EntryInline(admin.StackedInline):
#   model = Entry.prediction.through
#   extra = 1

# class PredictionAdmin(admin.ModelAdmin):
#   inlines = [EntryInline]


class EntryAdmin(admin.ModelAdmin):
  # filter_horizontal = ("finalists", "top_scorers")
  pass


admin.site.register(Entry, EntryAdmin)
admin.site.register(Prediction)
admin.site.register(Finalist)
admin.site.register(TopScorer)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Fixture)
admin.site.register(Result)
admin.site.register(Score)
