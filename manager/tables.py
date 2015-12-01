import django_tables2 as tables
from django_tables2.utils import A

from django.utils.safestring import mark_safe
from django.utils.html import escape

from .models import *

class FollowupsTable(tables.Table):
    #description = tables.LinkColumn()
    class Meta:
        model = Followup_Item
        attrs = {'class':'followups'}
        sequence = ("description", "date_due")
        fields = ("description", "date_due")

class UpcomingEvents(tables.Table):
    title = tables.LinkColumn('manager:viewEvent', args=[A('pk')])
    class Meta:
        model = Event
        attrs = {'class':'events'}
        fields = ("title", "date_event_start", "date_event_end")
        
