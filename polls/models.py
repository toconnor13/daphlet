from django.db import models
import datetime
from django.utils import timezone
from django.forms import ModelForm

# Create your models here.
class Poll(models.Model):
	question = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date_published')
	has_voted_list = models.CommaSeparatedIntegerField(max_length=1000000)
	restrict_to_domain = models.CharField(max_length=200, default="None")
	restricts_to_emails = models.charField(max_length=8000, default="None")

	def __unicode__(self):
		return self.question

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = "Published recently?"
	
	def vote_count(self):
		vote_count = 0
		for choice in self.choice_set.all():
			vote_count += choice.votes
		return vote_count
	vote_count.short_description = "Votes"

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice = models.CharField(max_length=200)
	votes = models.IntegerField()

	def __unicode__(self):
		return self.choice

class PollForm(ModelForm):
	class Meta:
		model=Poll

