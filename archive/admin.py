from django.contrib import admin
from django.forms import Textarea
from easy_select2 import select2_modelform

# Register your models here.
from .models import *

EventForm = select2_modelform(Event, attrs={'width': '250px'})
ResultForm = select2_modelform(Result, attrs={'width': '150px'})
AliasForm = select2_modelform(Alias, attrs={'width':'250px'})

class ResultInline(admin.TabularInline):
    model = Result
    form = ResultForm
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

    def get_extra(self, request, obj=None, **kwargs):
        return 15

class EventAdmin(admin.ModelAdmin):
    inlines = [ResultInline,]
    form = EventForm

class ResultAdmin(admin.ModelAdmin):
    form = ResultForm

class AliasAdmin(admin.ModelAdmin):
    form = AliasForm

admin.site.register(Runner)
admin.site.register(Event, EventAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Course)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Series)