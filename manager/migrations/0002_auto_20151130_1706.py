# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('first_name', 'last_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='email',
            unique_together=set([('email',)]),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('address', 'city', 'state')]),
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='outreach',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('phone',)]),
        ),
        migrations.AlterUniqueTogether(
            name='website',
            unique_together=set([('website_url',)]),
        ),
    ]
