from django.db import models
from django.contrib.auth.models import User

'''Model:
 - Outreach
  -- Contact
  -- Follow-up
  -- Event

 - Contact
  -- Organization (Many to Many)
  -- Email
  -- Phone
  -- Website
  -- Location (Many to Many)
  -- Interaction
  -- Follow Up Item
  -- Comment
  -- TIE TO EVENTS (Many to Many)

 - Location
 
 - Events
  -- Location (One to Many)
  -- Comment
'''

class Contact(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    first_name = models.TextField()
    last_name = models.TextField()
    notes = models.TextField(blank = True, null = True)

    def __str__(self):
        return "{0} {1}".format(self.first_name,
                                self.last_name)

    def getCurrentJob(self):
        try:
            result = self.job_set.filter(current=True)[0]
        except IndexError:
            result = None
        return result

    class Meta:
        unique_together = (('first_name', 'last_name'))

class Job(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    contact_pk = models.ForeignKey(Contact, blank = True, null = True)
    org_pk = models.ForeignKey("Organization", blank = True, null = True)
    job = models.TextField(blank = True, null = True)
    notes = models.TextField(blank = True, null = True)
    current = models.BooleanField(default = False)

    def __str__(self):
        return "{0}, {1}".format(self.job, self.org_pk)
    

class Email(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='user_creator')
    contact_pk = models.ForeignKey(Contact, blank=True, null=True)
    primary = models.BooleanField(default = False)
    description = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return "{0}: {1}, Primary: {2}".format(self.description,
                                               self.email,
                                               self.primary)
    class Meta:
        unique_together = (('email',))

class Phone(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    contact_pk = models.ForeignKey(Contact)
    primary = models.BooleanField(default=False)
    description = models.TextField()
    phone = models.TextField()
    
    def __str__(self):
        return "{0}: {1}, Primary: {2}".format(self.description,
                                               self.phone,
                                               self.primary)
    class Meta:
        unique_together = (('phone',))

class Website(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    description = models.TextField()
    website_url = models.URLField()
    contact_pk = models.ManyToManyField(Contact, blank = True)
    event_pk = models.ManyToManyField("Event", blank=True)
    org_pk = models.ManyToManyField("Organization", blank=True)

    def __str__(self):
        return "{0}: {1}".format(self.description,
                                 self.website_url)

    class Meta:
        unique_together = (('website_url',))

class Location(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    contact_pk = models.ManyToManyField(Contact, blank=True)
    event_pk = models.ManyToManyField("Event", blank=True)
    org_pk = models.ManyToManyField("Organization", blank=True)
    name = models.TextField()
    address = models.TextField(blank = True, null = True)
    city = models.TextField()
    state = models.TextField()

    def __str__(self):
        return "{0}: {1}, {2}".format(self.name,
                                      self.city,
                                      self.state)
    class Meta:
        unique_together = (('address', 'city', 'state',))

class Event(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    date_event_start = models.DateField("Event Start")
    date_event_end = models.DateField("Event Ends", blank=True, null=True)
    title = models.TextField("Title")
    location_pk = models.ForeignKey(Location, blank=True, null=True)
    description = models.TextField("Description")

    def __str__(self):
        return "{0}: {1}".format(self.date_event_start,
                                 self.title)

class Interaction(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    contact_pk = models.ForeignKey(Contact, blank=True, null=True)
    event_pk = models.ForeignKey(Event, blank=True, null=True)
    notes = models.TextField()

    def __str__(self):
        return "{0}: {1}".format(self.contact_pk,
                                 self.event_pk)

class Followup_Item(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User, related_name='creator')
    contact_pk = models.ForeignKey(Contact, blank=True, null = True)
    event_pk = models.ForeignKey(Event, blank = True, null = True)
    date_due = models.DateField("Date Due", blank = True, null = True)
    time_due = models.TimeField(blank = True, null = True)
    description = models.TextField("Description")
    assigned_to = models.ForeignKey(User, blank = True, null = True, related_name='assigned_to')
    complete = models.BooleanField(default = False)

    def __str__(self):
        return "{0} ({1}) {2}, Complete: {3}".format(self.description,
                                                     self.assigned_to,
                                                     self.date_due,
                                                     self.complete)

class Organization(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    primary_contact = models.ForeignKey(Contact, blank=True, null=True)
    website_pk = models.ForeignKey(Website, blank=True, null=True)
    location_pk = models.ForeignKey(Location, blank=True, null=True)
    name = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        unique_together = (('name',))

class Outreach(models.Model):
    date_create=models.DateTimeField(auto_now_add=True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(User)
    owned_by = models.ForeignKey(User, related_name='owned_by')
    contact_pk = models.ManyToManyField(Contact, blank=True)
    event_pk = models.ManyToManyField(Event, blank=True)
    follow_pk = models.ManyToManyField(Followup_Item, blank=True)
    name = models.TextField()

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        unique_together = (('name',))

class ModelComment(models.Model):
    ##This is the class for the comments that each individual comment model builds on
    date_create = models.DateTimeField(auto_now_add = True)
    date_mod = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    within_pk = models.ForeignKey('self', blank = True, null = True)
    comment = models.TextField("Add Comment")

    def __str__(self):
        return '{0}, {1}: "{2}"'.format(self.date_create, self.created_by, self.comment)

class Followup_Comment(ModelComment):
    fu_pk = models.ForeignKey(Followup_Item)

class Organization_Comment(ModelComment):
    o_pk = models.ForeignKey(Organization)

class Event_Comment(ModelComment):
    e_pk = models.ForeignKey(Event)

class Contact_Comment(ModelComment):
    c_pk = models.ForeignKey(Contact)

class Outreach_Comment(ModelComment):
    out_pk = models.ForeignKey(Outreach)
