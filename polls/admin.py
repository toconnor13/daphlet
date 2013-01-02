from polls.models import Poll
from django.contrib import admin
from polls.models import Choice

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class PollAdmin(admin.ModelAdmin):
	fieldsets = [
			(None, 	{'fields': ['question']}),
			('Date information',	{'fields': ['pub_date']}),

	]
	inlines = [ChoiceInline]
	list_display = ('question','pub_date','was_published_recently', 'vote_count')

admin.site.register(Poll, PollAdmin)
