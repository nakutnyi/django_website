"""Define what's available for admin modifications"""
from django.contrib import admin

from .models import Question, Choice


# Register models

class ChoiceInline(admin.TabularInline):
    """Allow choices modification within the Question panel"""

    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    """Define how Question panel looks"""

    fields = ['text', 'dt_published']
    inlines = [ChoiceInline]
    list_display = ('text', 'dt_published', 'is_recent')
    list_filter = ['dt_published']
    search_fields = ['text']


admin.site.register(Question, QuestionAdmin)