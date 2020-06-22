from django.contrib import admin
from .models import Team, Player, Fixture, Result, Score, Prediction, Finalist, TopScorer, Entry


# class EntryInline(admin.StackedInline):
#   model = Entry.prediction.through
#   extra = 1

# class PredictionAdmin(admin.ModelAdmin):
#   inlines = [EntryInline]

class EntryAdmin(admin.ModelAdmin):
  filter_horizontal = ("predictions", "finalists", "top_scorers")


admin.site.register(Entry, EntryAdmin)
admin.site.register(Prediction)
admin.site.register(Finalist)
admin.site.register(TopScorer)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Fixture)
admin.site.register(Result)
admin.site.register(Score)