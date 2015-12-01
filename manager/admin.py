from django.contrib import admin

from .models import *

class ContactsInline(admin.StackedInline):
    model = Contact

admin.site.register(Contact)
admin.site.register(Organization)
admin.site.register(Email)
admin.site.register(Phone)
admin.site.register(Website)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Interaction)
admin.site.register(Followup_Item)
admin.site.register(Followup_Comment)
admin.site.register(Outreach)
