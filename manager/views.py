from django.shortcuts import render
from django.http import HttpResponseRedirect
from django_tables2 import RequestConfig
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse

from django.contrib.auth import views
from django.contrib.auth.models import User

import datetime

from .models import *
from .forms import *
from .tables import *

def index(request):
    fuTable = makeFuTable(request)
    data = makeOutreachSummaryTable()
    events = Event.objects.filter(date_event_start__gte = datetime.datetime.now()).filter(date_event_end__gte = datetime.datetime.now())
    if len(events) == 0:
        eventTable = None
    else:
        eventTable = UpcomingEvents(events)
        RequestConfig(request, paginate=False).configure(eventTable)
    statData = makeSummaryStatsDic()
    context = RequestContext(request, {'allOutreach': data,
                                       'fuTable':fuTable,
                                       'events':eventTable,
                                       'stats': statData})
    return render(request, 'index.html', context)

@login_required
def addOutreach(request, pk=None):
    data = None
    if pk is not None:
        data = Outreach.objects.get(pk=pk)
    if request.method == "POST":
        form = AddOutreachForm(request.POST, instance=data)
        if form.is_valid():
            o = form.save(commit=False)
            user = User.objects.get(pk=request.user.id)
            o.created_by = user
            o.save()
            form.save_m2m()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:viewOutreach', args=[o.id]))
    else:
        form = AddOutreachForm(instance=data)
    
    context = RequestContext(request, {'outreach':form})
    return render(request, 'addOutreach.html', context)

def viewOutreach(request, pk):
    outreach = Outreach.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentOutreachForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.out_pk = Outreach.objects.get(pk = request.POST['oPk'])
            f.created_by = request.user
            f.save()
            return HttpResponseRedirect(reverse('manager:viewOutreach', args=[pk]))
    else:
        form = CommentOutreachForm()
    context = RequestContext(request, {'outreach':outreach, 'form_comment':form})
    return render(request, 'viewOutreach.html', context)

def viewAllOutreach(request):
    fuTable = makeFuTable(request)
    allOutreach = Outreach.objects.all()
    data = makeOutreachSummaryTable()
    context = RequestContext(request, {'allOutreach': data,
                                       'fuTable':fuTable})
    return render(request, 'viewAllOutreach.html', context)

@login_required
def addOrg(request, pk=None):
    data = None
    if pk is not None:
        data = Organization.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddOrganizationForm(request.POST, instance=data)
        if form.is_valid():
            o = form.save(commit = False)
            userObj = User.objects.get(pk=request.user.id)
            o.created_by = request.user
            newWeb = form.cleaned_data['website_other']
            if newWeb!="":
                web = Website.objects.create(created_by=request.user,
                                             website_url = newWeb)
                o.website_pk = web
            o.save()
            form.save_m2m()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:viewOrg', args=[o.id]))
    else:
        form = AddOrganizationForm(instance=data)
    context = RequestContext(request, {'org':form})
    return render(request, 'addOrg.html', context)

def viewAllOrgs(request):
    orgs = Organization.objects.all()
    data = []
    for o in orgs:
        data.append({'id':o.id,
                     'name':o.name,
                     'primary_contact':o.primary_contact,
                     'website_pk':o.website_pk})
    context = RequestContext(request, {'orgs':data})
    return render(request, 'viewAllOrgs.html', context)

def viewOrg(request, pk):
    data = Organization.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentOrgForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.o_pk = Organization.objects.get(pk = request.POST['oPk'])
            f.created_by = request.user
            f.save()
            return HttpResponseRedirect(reverse('manager:viewOrg', args=[pk]))
    else:
        form = CommentOrgForm()
    context = RequestContext(request, {'org':data, 'form': form})
    return render(request, 'viewOrg.html', context)

@login_required
def addEvent(request, pk = None, pkForOutreach = None, pkForContact = None):
    data = None
    if pk is not None:
        data = Event.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddEventForm(request.POST, instance=data)
        if form.is_valid():
            e = form.save(commit=False)
            userObj = User.objects.get(pk=request.user.id)
            e.created_by = request.user
            e.save()
            if pkForOutreach is not None:
                out = Outreach.objects.get(pk = pkForOutreach)
                out.event_pk.add(e)
            if pkForContact is not None:
                contact = Outreach.objects.get(pk = pkForContact)
                out.contact_pk = contact
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:viewEvent', args=[e.id]))
    else:
        form = AddEventForm(instance=data)
    context = RequestContext(request, {'event':form})
    return render(request, 'addEvent.html', context)

def viewEvent(request, pk):
    eventData = Event.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentEventForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.e_pk = Event.objects.get(pk = request.POST['ePk'])
            f.created_by = request.user
            f.save()
            return HttpResponseRedirect(reverse('manager:viewEvent', args=[pk]))
    else:
        form = CommentEventForm()
    context = RequestContext(request, {'event': eventData, 'form':form})
    return render(request, 'viewEvent.html', context)

def viewAllEvents(request):
    eventData = Event.objects.all()
    events = []
    for e in eventData:
        events.append({'id':e.id,
                       'title': e.title,
                       'description': e.description,
                       'location': e.location_pk,
                       'date_event_start': e.date_event_start,
                       'date_event_end': e.date_event_end})
    context = RequestContext(request, {'events':events})
    return render(request, 'viewAllEvents.html', context)

@login_required
def addInteraction(request, pkForContact=None, pk=None):
    data = None
    if pk is not None:
        interact = Interaction.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddInteractionForm(request.POST, instance=data)
        if form.is_valid():
            e = form.save(commit=False)
            e.created_by = request.user
            if pkForContact is not None:
                e.contact_pk = Contact.objects.get(pk=pkForContact)
            e.save()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:viewContact', args=[pkForContact]))
    else:
        form = AddInteractionForm(instance=data)
    context = RequestContext(request, {'form': form})
    return render(request, 'addInteraction.html', context)

@login_required
def addFollowup(request, pk = None, pkForOutreach = None, pkForContact = None):
    data = None
    if pk is not None:
        data = Followup_Item.objects.get(pk = pk)
    if request.method == 'POST':
        form = AddFollowupForm(request.POST, instance = data)
        if form.is_valid():
            p = form.save(commit=False)
            p.created_by = request.user
            if pkForContact is not None:
                p.contact_pk = Contact.objects.get(pk = pkForContact)
            p.save()
            if pkForOutreach is not None:
                out = Outreach.objects.get(pk = pkForOutreach)
                out.follow_pk.add(p)
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:viewAllFollowups'))
    else:
        form = AddFollowupForm(instance = data)
    context = RequestContext(request, {'form':form})
    return render(request, 'addFollowup.html', context)

def viewAllFollowups(request):
    data = Followup_Item.objects.filter(complete = False).order_by('date_due')
    if request.method == 'POST':
        form = CommentFollowupForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.fu_pk = Followup_Item.objects.get(pk = request.POST['fuPk'])
            f.created_by = request.user
            f.save()
            return HttpResponseRedirect(reverse('manager:viewAllFollowups'))
    else:
        form = CommentFollowupForm()
    context = RequestContext(request, {'followups':data, 'form':form})
    return render(request, 'viewAllFollowups.html', context)

def markComplete(request, pk):
    data = Followup_Item.objects.get(pk=pk)
    data.complete = True
    data.save()
    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET['next'])
    return HttpResponseRedirect(reverse('manager:index'))

@login_required
def addContact(request, pkForOutreach = None):
    ##Some sub-forms are not getting saved.
    if request.method == 'POST':
        acForm = AddContactForm(request.POST, prefix="ac")
        aeForm = AddEmailForm(request.POST, prefix="ae")
        apForm = AddPhoneForm(request.POST, prefix="ap")
        ajForm = AddJobForm(request.POST, prefix="aj")
        if acForm.is_valid():
            c = acForm.save(commit=False)
            c = setUserAndSave(c, request.user)
            if aeForm.is_valid():
                e = aeForm.save(commit=False)
                e.contact_pk = c
                e = setUserAndSave(e, request.user)
            if apForm.is_valid():
                p = apForm.save(commit=False)
                p.contact_pk = c
                p = setUserAndSave(p, request.user)
            if ajForm.is_valid():
                j = ajForm.save(commit=False)
                j.contact_pk = c
                newOrg = ajForm.cleaned_data['org_other']
                if newOrg != "":
                    o = Organization.objects.create(created_by = request.user,
                                                    name = newOrg)
                    j.org_pk = o
                j = setUserAndSave(j, request.user)
            if pkForOutreach is not None:
                out = Outreach.objects.get(pk = pkForOutreach)
                out.contact_pk.add(c)
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:viewContact', args=[c.id]))
    else:
        acForm = AddContactForm(prefix="ac")
        aeForm = AddEmailForm(prefix="ae")
        apForm = AddPhoneForm(prefix="ap")
        ajForm = AddJobForm(prefix="aj")
    return render(request, 'addContact.htm', {'acForm': acForm,
                                              'aeForm': aeForm,
                                              'apForm': apForm,
                                              'ajForm': ajForm,
                                              'user': request.user})

@login_required
def editContact(request, pk):
    data = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddContactForm(request.POST, instance=data)
        if form.is_valid():
            c = form.save(commit=False)
            c = setUserAndSave(c, request.user)
            form.save_m2m()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:viewContact', args=[data.id]))
    else:
        form = AddContactForm(instance=data)
    context = RequestContext(request, {'form':form, 'pk':data.id})
    return render(request, 'addContactOnly.html', context)

def viewAllContacts(request):
    contacts = Contact.objects.all().order_by('last_name')
    out = []
    for c in contacts:
        jobData = getJobFromContact(c)
        out.append({'id': c.id,
                    'name': c.last_name + ", " + c.first_name,
                    'job': jobData[1],
                    'org': jobData[0],
                    'nInteract': len(c.interaction_set.all()),
                    'nFollowup': len(c.followup_item_set.filter(complete=False))})
    context = RequestContext(request, {'contacts':out})
    return render(request, 'viewAllContacts.html', context)

def getJobFromContact(c):
    try:
        jobDescribe = c.job_set.filter(current = True)[0]
        jobData = [jobDescribe.org_pk, jobDescribe.job]
    except IndexError:
        jobData = ["No Data", "No Data"]
    return jobData

@login_required
def viewContact(request, pk):
    contact = Contact.objects.get(pk=pk)
    if contact is None:
        return HttpResponseRedirect(reverse('manager:index'))
    if request.method == 'POST':
        form = AddInteractionForm(request.POST)
        if form.is_valid():
            e = form.save(commit=False)
            e.created_by = request.user
            e.contact_pk = contact
            e.save()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:viewContact', args=[contact.id]))
        form_comment = CommentContactForm(request.POST)
        if form_comment.is_valid():
            f = form_comment.save(commit=False)
            f.c_pk = Contact.objects.get(pk = request.POST['cPk'])
            f.created_by = request.user
            f.save()
            return HttpResponseRedirect(reverse('manager:viewContact', args=[contact.id]))
    else:
        form = AddInteractionForm()
        form_comment = CommentContactForm()
    #addToForm = AddToAnythingContactForm()
    context = RequestContext(request, {'contact':contact,
                                       'pk':pk,
                                       'form': form,
                                       #'addToForm': addToForm,
                                       'form_comment': form_comment})
    return render(request, 'viewContact.html', context)

@login_required
def addJobToContact(request, pk, pkForJob = None):
    jobData = None
    if pkForJob is not None:
        jobData = Job.objects.get(pk = pkForJob)
    data = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddJobForm(request.POST, instance=jobData)
        if form.is_valid():
            p = form.save(commit=False)
            userObj = User.objects.get(pk=request.user.id)
            p.created_by = request.user
            p.contact_pk = data
            p.save()
            return HttpResponseRedirect(reverse('manager:viewContact', args=[pk]))
    else:
        form = AddJobForm(instance=jobData)
    context = RequestContext(request, {'form':form,
                                       'data':data,
                                       'datatype':'Job'})
    return render(request, 'addSomethingToContact.html', context)

@login_required
def addPhoneToContact(request, pk, pkForPhone = None):
    phoneData = None
    if pkForPhone is not None:
        phoneData = Phone.objects.get(pk = pkForPhone)
    data = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddPhoneForm(request.POST, instance=phoneData)
        if form.is_valid():
            p = form.save(commit=False)
            userObj = User.objects.get(pk=request.user.id)
            p.created_by = request.user
            p.contact_pk = data
            p.save()
            return HttpResponseRedirect(reverse('manager:viewContact', args=[pk]))
    else:
        form = AddPhoneForm(instance=phoneData)
    context = RequestContext(request, {'form':form,
                                       'data':data,
                                       'datatype':'Phone'})
    return render(request, 'addSomethingToContact.html', context)

@login_required
def addEmailToContact(request, pk, pkForEmail = None):
    emailData = None
    if pkForEmail is not None:
        emailData = Email.objects.get(pk = pkForEmail)
    data = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddEmailForm(request.POST, instance=emailData)
        if form.is_valid():
            p = form.save(commit=False)
            userObj = User.objects.get(pk=request.user.id)
            p.created_by = request.user
            p.contact_pk = data
            p.save()
            return HttpResponseRedirect(reverse('manager:viewContact', args=[pk]))
    else:
        form = AddEmailForm(instance = emailData)
    context = RequestContext(request, {'form':form,'data':data,
                                       'datatype':'Email'})
    return render(request, 'addSomethingToContact.html', context)

@login_required
def addOutreachToContact(request, pk):
    data = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddOutreachToContactForm(request.POST)
        if form.is_valid():
            out = form.cleaned_data['outreaches']
            if out != "---":
                outreach = Outreach.objects.get(pk = out)
                outreach.contact_pk.add(data)
            
            return HttpResponseRedirect(reverse('manager:viewContact', args=[pk]))
    else:
        form = AddOutreachToContactForm()
    context = RequestContext(request, {'form':form,'data':data,
                                       'datatype':'Outreach or Event'})
    return render(request, 'addSomethingToContact.html', context)

@login_required
def addWebsite(request, pk = None, pkForWebsite = None):
    websiteData = None
    if pkForWebsite is not None:
        websiteData = Website.objects.get(pk=pkForWebsite)
    if request.method == 'POST':
        form = AddWebsiteForm(request.POST, instance=websiteData)
        if form.is_valid():
            p = form.save(commit=False)
            userObj = User.objects.get(pk=request.user.id)
            p.created_by = request.user
            p.save()
            if pk is not None:
                p.contact_pk.add(Contact.objects.get(pk=pk))
            p.save()
            form.save_m2m()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:index'))
    else:
        form = AddWebsiteForm(instance = websiteData)
    context = RequestContext(request, {'form':form, 'datatype':'Website'})
    return render(request, 'addSomething.html', context)

@login_required
def addLocation(request, pk = None, pkForLocation = None):
    locationData = None
    if pkForLocation is not None:
        locationData = Location.objects.get(pk = pkForLocation)
    if request.method == 'POST':
        form = AddLocationForm(request.POST, instance=locationData)
        if form.is_valid():
            l = form.save(commit = False)
            l.created_by = request.user
            l.save()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('manager:index'))
    else:
        form = AddLocationForm(instance = locationData)
    context = RequestContext(request, {'form':form, 'datatype':'Location'})
    return render(request, 'addSomething.html', context)

def makeFuTable(request):
    upcomingFu = Followup_Item.objects.filter(date_due__gte = datetime.datetime.now(),
                                              complete = False).order_by('date_due')
    fuTable = FollowupsTable(upcomingFu)
    RequestConfig(request, paginate = False).configure(fuTable)
    if len(upcomingFu) == 0:
        return None
    return fuTable

def makeSummaryStatsDic():
    statData = []
    c = Contact.objects.all()
    c_new = c.filter(date_create__gte = (datetime.datetime.now()- datetime.timedelta(days=30)))
    statData = packStatData(statData, 'Contacts', len(c), len(c_new))
    
    i = Interaction.objects.all()
    i_new = i.filter(date_create__gte = (datetime.datetime.now()-datetime.timedelta(days=30)))
    if len(c_new) == 0:
        statData = packStatData(statData, 'Interactions', 0, 0)
    else:
        statData = packStatData(statData, 'Interactions', len(i)+1, len(i_new)+len(c_new))
    
    e = Event.objects.all()
    e_new = e.filter(date_event_start__gte = (datetime.datetime.now() - datetime.timedelta(days=30)))
    statData = packStatData(statData, 'Events (all)', len(e), len(e_new))
    
    events = Event.objects.filter(date_event_start__gte = datetime.datetime.now()).filter(date_event_end__gte = datetime.datetime.now())
    events_new = events.filter(date_event_start__lte = (datetime.datetime.now() + datetime.timedelta(days=30)))
    statData = packStatData(statData, 'Events (upcoming)', len(events), '{0} <br />(next 30)'.format(len(events_new)))

    o = Organization.objects.all()
    o_new = o.filter(date_create__gte = (datetime.datetime.now() - datetime.timedelta(days=30)))
    statData = packStatData(statData, 'Orgs', len(o), len(o_new))
    return statData

def packStatData(li, statName, val1, val2):
    li.append({'StatName': statName,
                     'Stat': val1,
                     'StatRecent': val2})
    return li

def setUserAndSave(obj, req_user):
    userObj = User.objects.get(pk=req_user.id)
    obj.created_by = userObj
    obj.save()
    return obj

def makeOutreachSummaryTable():
    allOutreach = Outreach.objects.all()
    data = []
    for o in allOutreach:
        nInteract = 0
        nFollowup = 0
        for x in o.contact_pk.all():
            nInteract += len(x.interaction_set.all())
            nFollowup += len(x.followup_item_set.all())
        data.append({'id':o.id,
                     'name':o.name,
                     'nInteract':nInteract,
                     'nContact':len(o.contact_pk.all()),
                     'nEvent':len(o.event_pk.all()),
                     'nOpenFu':len(o.follow_pk.filter(complete=False))+nFollowup})
    return data
