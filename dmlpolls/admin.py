from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	#fieldsets = [
    #    (None,               {'fields': ['question_text']}),
	#	(None,               {'fields': ['author']}),
    #    (None, 				{'fields': ['pub_date']}),
    #]
	inlines = [ChoiceInline]
	list_display = ('question_text', 'author', 'pub_date', 'was_published_recently', )
	search_fields = ['question_text']
	#search_fields = ['author']
	date_hierarchy = 'pub_date'

admin.site.register(Question, QuestionAdmin)
