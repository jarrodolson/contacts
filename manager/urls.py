from django.conf.urls import url

from . import views

basicPatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addWebsite/$', views.addWebsite, name='addWebsite'),
    ]
outreachPatterns= [
    url(r'^addOutreach/$',
        views.addOutreach,
        name='addOutreach'),
    url(r'^editOutreach/(?P<pk>[0-9]+)/$',
        views.addOutreach,
        name='addOutreach'),
    url(r'^addEventToOutreach/(?P<pkForOutreach>[0-9]+)/$',
        views.addEvent,
        name='addEventToOutreach'),
    url(r'^addFollowupToOutreach/(?P<pkForOutreach>[0-9]+)/$',
        views.addFollowup,
        name='addFollowupToOutreach'),
    ]

contactPatterns = [
    url(r'^addContact/$',
        views.addContact,
        name='addContact'),
    url(r'^editContact/(?P<pk>[0-9]+)/$',
        views.editContact,
        name='editContact'),
    url(r'^addContactToOutreach/(?P<pkForOutreach>[0-9]+)/$',
        views.addContact,
        name='addContactToOutreach'),
    url(r'^addEventToContact/(?P<pkForContact>[0-9]+)/$',
        views.addEvent,
        name='addEventToContact'),
    url(r'^addEmailToContact/(?P<pk>[0-9]+)/$',
        views.addEmailToContact,
        name='addEmailToContact'),
    url(r'^editEmailToContact/(?P<pk>[0-9]+)/(?P<pkForEmail>[0-9]+)/$',
        views.addEmailToContact,
        name='editContactEmail'),
    url(r'^addFollowupToContact/(?P<pkForContact>[0-9]+)/$',
        views.addFollowup,
        name='addFollowupToContact'),
    url(r'^editFollowupForContact/(?P<pkForContact>[0-9]+)/(?P<pk>[0-9]+)/$',
        views.addFollowup,
        name='editContactFollowup'),
    url(r'^addJobToContact/(?P<pk>[0-9]+)/$',
        views.addJobToContact,
        name='addJobToContact'),
    url(r'^addJobToContact/(?P<pk>[0-9]+)/(?P<pkForJob>[0-9]+)/$',
        views.addJobToContact,
        name='editContactJob'),
    url(r'^addPhoneToContact/(?P<pk>[0-9]+)/$',
        views.addPhoneToContact,
        name='addPhoneToContact'),
    url(r'^editPhoneToContact/(?P<pk>[0-9]+)/(?P<pkForPhone>[0-9]+)/$',
        views.addPhoneToContact,
        name='editContactPhone'),
    
    url(r'^addOutreachToContact/(?P<pk>[0-9]+)/$',
        views.addOutreachToContact,
        name='addOutreachToContact'),
    url(r'^editOutreachToContact/(?P<pk>[0-9]+)/(?P<pkForOutreach>[0-9]+)/$',
        views.addOutreachToContact,
        name='editOutContact'),

    url(r'^addWebToContact/(?P<pk>[0-9]+)/$',
        views.addWebsite,
        name='addWebsiteToContact'),
    url(r'^editWebToContact/(?P<pk>[0-9]+)/(?P<pkForWebsite>[0-9]+)/$',
        views.addWebsite,
        name='editContactWebsite'),
    ]

orgPatterns = [
    url(r'^addOrg/$', views.addOrg, name = 'addOrg'),
    url(r'^editOrg/(?P<pk>[0-9]+)/$', views.addOrg, name='editOrg'),
    ]

eventPatterns = [
    url(r'^addEvent/$', views.addEvent, name='addEvent'),
    url(r'^editEvent/(?P<pk>[0-9]+)/$', views.addEvent, name='editEvent'),
    ]

followupPatterns = [
    url(r'^viewAllFollowups/$', views.viewAllFollowups, name='viewAllFollowups'),
    url(r'^addFollowup/$', views.addFollowup, name='addFollowup'),
    url(r'^editFollowup/(?P<pk>[0-9]+)/$', views.addFollowup, name='addFollowup'),
    url(r'^markFollowupComplete/(?P<pk>[0-9]+)/$', views.markComplete, name='markFuComplete'),
    ]

viewAggregatePatterns = [
     url(r'^viewAllContacts/$', views.viewAllContacts, name = 'viewAllContacts'),
     url(r'^viewAllOutreach/$', views.viewAllOutreach, name='viewAllOutreach'),
     url(r'^viewAllEvents/$', views.viewAllEvents, name='viewAllEvents'),
     url(r'^viewAllOrgs/$', views.viewAllOrgs, name='viewAllOrgs'),
    ]

viewDetailPatterns = [
    url(r'^viewContact/(?P<pk>[0-9]+)/$', views.viewContact, name='viewContact'),
    url(r'^viewEvent/(?P<pk>[0-9]+)/$', views.viewEvent, name='viewEvent'),
    url(r'^viewOrg/(?P<pk>[0-9]+)/$', views.viewOrg, name='viewOrg'),
    url(r'^viewOutreach/(?P<pk>[0-9]+)/$', views.viewOutreach, name='viewOutreach'),
    ]
interactionPatterns = [
    url(r'^addInteraction/(?P<pkForContact>[0-9]+)/$',
        views.addInteraction,
        name='addInteraction'),
    url(r'^editInteraction/(?P<pkForContact>[0-9]+)/(?P<pk>[0-9]+)/$',
        views.addInteraction,
        name='editInteraction'),
    ]

locationPatterns = [
    url(r'^addLocation/$',
        views.addLocation,
        name='addLocation'),
    url(r'^editLocation/(?P<pkForLocation>[0-9]+)/$',
        views.addLocation,
        name='addLocation'),
    ]


urlpatterns = basicPatterns + outreachPatterns + contactPatterns + orgPatterns + eventPatterns + followupPatterns + viewAggregatePatterns + viewDetailPatterns + interactionPatterns + locationPatterns
