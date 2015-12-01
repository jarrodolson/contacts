from django import forms
from django.contrib.admin import widgets
from django.forms import formsets, Textarea

from .models import *

TEXTAREA_ROWS = 4
TEXTAREA_COLS = 50

##WIDGETS
class CustomRelatedFieldWidgetWrapper(widgets.RelatedFieldWidgetWrapper):

    """
        Based on RelatedFieldWidgetWrapper, this does the same thing
        outside of the admin interface

        the parameters for a relation and the admin site are replaced
        by a url for the add operation
    """

    def __init__(self, widget, add_url,permission=True):
        self.is_hidden = widget.is_hidden
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.add_url = add_url
        self.permission = permission

    def render(self, name, value, *args, **kwargs):
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.permission:
            output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                (self.add_url, name))
            output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))

class AddToAnythingContactForm(forms.Form):
    contact = forms.ChoiceField(label='Add to Contact', choices = Contact.objects.all())
    event = forms.ChoiceField(label = 'Add to Events', choices = Contact.objects.all())

class AddContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        #fields = ['first_name']
        exclude = ['date_create', 'date_mod', 'created_by']
        
        widgets = {
            'first_name': forms.widgets.TextInput(),
            'last_name': forms.widgets.TextInput(),
            'notes': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                     'cols':TEXTAREA_COLS})
            }
        
class CommentContactForm(forms.ModelForm):
    class Meta:
        model = Contact_Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                       'cols':TEXTAREA_COLS}),
            }


class AddOrganizationForm(forms.ModelForm):
    ##Add extra fields to get location and website information
    ## during save, check that it doesn't already exist, if it does, assign
    ## existing key
    website_other = forms.CharField(required=False)
    class Meta:
        model = Organization
        exclude = ['date_create', 'date_mod', 'created_by']
        fields = ['name', 'website_pk', 'website_other', 'primary_contact', 'location_pk',  'notes']
        
        widgets = {
            'name': forms.widgets.TextInput(),
            'notes': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                     'cols':TEXTAREA_COLS}),
            }

class CommentOrgForm(forms.ModelForm):
    class Meta:
        model = Organization_Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                       'cols':TEXTAREA_COLS}),
            }

class AddJobForm(forms.ModelForm):
    org_other = forms.CharField(required=False)
    class Meta:
        model = Job
        exclude = ['date_create', 'date_mod', 'contact_pk', 'created_by']
        fields = ['org_pk', 'org_other', 'job', 'notes', 'current']
        
        widgets = {
            'job': forms.widgets.TextInput(),
            'notes': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                     'cols':TEXTAREA_COLS})
            }

class AddEmailForm(forms.ModelForm):
    class Meta:
        model = Email
        exclude = ['date_create', 'date_mod', 'contact_pk', 'created_by']
        fields = ['description', 'email', 'primary']
        
        widgets = {
            'description': forms.widgets.TextInput(),
            'email': forms.widgets.TextInput(),
            }

class AddOutreachToContactForm(forms.Form):

    def getDynamicChoices_outreach(self):
        raw = Outreach.objects.all()
        first = [('---', '---')]
        c = [(x.id, x.name) for x in raw]
        c = first + c
        return(c)

    def __init__(self, *args):
        super(AddOutreachToContactForm, self).__init__(*args)
        self.fields['outreaches'] = forms.ChoiceField(label = "Outreach Options", choices = self.getDynamicChoices_outreach())

class AddPhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ['date_create', 'date_mod', 'contact_pk', 'created_by']
        fields = ['description', 'phone', 'primary']
        
        widgets = {
            'description': forms.widgets.TextInput(),
            'phone': forms.widgets.TextInput(),
            }

class AddWebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        exclude = ['date_create', 'date_mod', 'contact_pk', 'created_by']
        widgets = {
            'description': forms.widgets.TextInput(),
            }
        
class AddInteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        exclude = ['date_create', 'date_mod', 'contact_pk', 'created_by']
        
        widgets = {
            'notes': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                     'cols':TEXTAREA_COLS}),
            }

class AddFollowupForm(forms.ModelForm):
    class Meta:
        model = Followup_Item
        exclude = ['date_create', 'date_mod', 'contact_pk', 'created_by']
        
        widgets = {
            'description': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                           'cols':TEXTAREA_COLS}),
            }

class CommentFollowupForm(forms.ModelForm):
    class Meta:
        model = Followup_Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                       'cols':TEXTAREA_COLS}),
            }

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['date_create', 'date_mod', 'created_by']
        widgets = {
            'title': forms.widgets.TextInput(),
            'description': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                           'cols':TEXTAREA_COLS})
            }

class CommentEventForm(forms.ModelForm):
    class Meta:
        model = Event_Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                       'cols':TEXTAREA_COLS}),
            }

class AddOutreachForm(forms.ModelForm):
    class Meta:
        model = Outreach
        fields = ['owned_by', 'name', 'contact_pk', 'event_pk', 'follow_pk']
        exclude = ['date_create', 'date_mod', 'created_by']
        widgets = {
            'name': forms.widgets.TextInput(),
            }

class CommentOutreachForm(forms.ModelForm):
    class Meta:
        model = Outreach_Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                       'cols':TEXTAREA_COLS}),
            }

class AddLocationForm(forms.ModelForm):
    class Meta:
        states = (('---', '---'),('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))
        model = Location
        exclude = ['date_create', 'date_mod', 'created_by']
        widgets = {
            'name': forms.widgets.TextInput(),
            'address': Textarea(attrs={'rows':TEXTAREA_ROWS,
                                       'cols':TEXTAREA_COLS}),
            'city': forms.widgets.TextInput(),
            'state': forms.widgets.Select(choices = states),
            }
