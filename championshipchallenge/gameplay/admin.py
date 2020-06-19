from django.contrib import admin
from .models import Entry, Team, Player, Fixture, Result, Score


admin.site.register(Entry)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Fixture)
admin.site.register(Result)
admin.site.register(Score)