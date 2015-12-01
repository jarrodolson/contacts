# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('primary', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('contact_pk', models.ForeignKey(null=True, to='manager.Contact', blank=True)),
                ('created_by', models.ForeignKey(related_name='user_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('date_event_start', models.DateField(verbose_name='Event Start')),
                ('date_event_end', models.DateField(blank=True, null=True, verbose_name='Event Ends')),
                ('title', models.TextField(verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Followup_Item',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('date_due', models.DateField(blank=True, null=True, verbose_name='Date Due')),
                ('time_due', models.TimeField(blank=True, null=True)),
                ('description', models.TextField(verbose_name='Description')),
                ('complete', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(related_name='assigned_to', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('contact_pk', models.ForeignKey(null=True, to='manager.Contact', blank=True)),
                ('created_by', models.ForeignKey(related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('event_pk', models.ForeignKey(null=True, to='manager.Event', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField()),
                ('contact_pk', models.ForeignKey(null=True, to='manager.Contact', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event_pk', models.ForeignKey(null=True, to='manager.Event', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('job', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('current', models.BooleanField(default=False)),
                ('contact_pk', models.ForeignKey(null=True, to='manager.Contact', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('contact_pk', models.ManyToManyField(to='manager.Contact', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event_pk', models.ManyToManyField(to='manager.Event', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModelComment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(verbose_name='Add Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('location_pk', models.ForeignKey(null=True, to='manager.Location', blank=True)),
                ('primary_contact', models.ForeignKey(null=True, to='manager.Contact', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Outreach',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('contact_pk', models.ManyToManyField(to='manager.Contact', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event_pk', models.ManyToManyField(to='manager.Event', blank=True)),
                ('follow_pk', models.ManyToManyField(to='manager.Followup_Item', blank=True)),
                ('owned_by', models.ForeignKey(related_name='owned_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('primary', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('phone', models.TextField()),
                ('contact_pk', models.ForeignKey(to='manager.Contact')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('website_url', models.URLField()),
                ('contact_pk', models.ManyToManyField(to='manager.Contact', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event_pk', models.ManyToManyField(to='manager.Event', blank=True)),
                ('org_pk', models.ManyToManyField(to='manager.Organization', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact_Comment',
            fields=[
                ('modelcomment_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='manager.ModelComment', serialize=False)),
                ('c_pk', models.ForeignKey(to='manager.Contact')),
            ],
            bases=('manager.modelcomment',),
        ),
        migrations.CreateModel(
            name='Event_Comment',
            fields=[
                ('modelcomment_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='manager.ModelComment', serialize=False)),
            ],
            bases=('manager.modelcomment',),
        ),
        migrations.CreateModel(
            name='Followup_Comment',
            fields=[
                ('modelcomment_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='manager.ModelComment', serialize=False)),
                ('fu_pk', models.ForeignKey(to='manager.Followup_Item')),
            ],
            bases=('manager.modelcomment',),
        ),
        migrations.CreateModel(
            name='Organization_Comment',
            fields=[
                ('modelcomment_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='manager.ModelComment', serialize=False)),
            ],
            bases=('manager.modelcomment',),
        ),
        migrations.CreateModel(
            name='Outreach_Comment',
            fields=[
                ('modelcomment_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='manager.ModelComment', serialize=False)),
                ('out_pk', models.ForeignKey(to='manager.Outreach')),
            ],
            bases=('manager.modelcomment',),
        ),
        migrations.AddField(
            model_name='organization',
            name='website_pk',
            field=models.ForeignKey(null=True, to='manager.Website', blank=True),
        ),
        migrations.AddField(
            model_name='modelcomment',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='modelcomment',
            name='within_pk',
            field=models.ForeignKey(null=True, to='manager.ModelComment', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='org_pk',
            field=models.ManyToManyField(to='manager.Organization', blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='org_pk',
            field=models.ForeignKey(null=True, to='manager.Organization', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='location_pk',
            field=models.ForeignKey(null=True, to='manager.Location', blank=True),
        ),
        migrations.AddField(
            model_name='organization_comment',
            name='o_pk',
            field=models.ForeignKey(to='manager.Organization'),
        ),
        migrations.AddField(
            model_name='event_comment',
            name='e_pk',
            field=models.ForeignKey(to='manager.Event'),
        ),
    ]
