__author__ = 'Cameron Poole'
# Author:Cameron Poole
# Date  : 31/10/14
# Data models for dlb activity logger so far
# Copyright (C) 2014  Cameron Poole
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import date

from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(default="cameron.j.poole@health.wa.gov.au")


#This should actually inherit from USER but currently having issues
#TODO: Make class inherit from USER
class Linker(User):
    linkername = models.CharField(max_length=15, default="cameronp")


class Client(Person):
    phone = models.CharField(max_length=14)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Reminder():
    pass


class DLUId(models.Model):
    '''
    Information about a particular dlu id
    '''
    projectid = models.CharField(default='999999.99', max_length=10)


class Dataset(models.Model):
    """
    Stores data about each dataset
    """
    TYPE = (('CI', 'Core Infrastructure'),
            ('NI', 'Non-Core Infrastructure'),
            ('RN', 'Recurring'),
            ('A', 'Adhoc'),
            ('O', 'Other'))
    UPDATES = (('W', 'Weekly'),
               ('M', 'Monthly'),
               ('Q', 'Quarterly'),
               ('B', 'Bi-Annual'),
               ('Y', 'Yearly'),
               ('O', 'One off'),
               ('U', 'Unknown'))
    name = models.CharField(max_length=50)
    restricted = models.BooleanField(default=False)
    categories = models.CharField(max_length=20, choices=TYPE)
    contact = models.ManyToManyField(Client)
    update_cycle = models.CharField(max_length=12, choices=UPDATES, default='Unknown')
    dlb_project_id = models.OneToOneField(DLUId)
    overview = models.TextField(default="This is a dataset overview")
    created_by = models.ManyToManyField(Linker)

    def __str__(self):
        return "Dataset {}".format(self.name)


class Update(models.Model):
    """
    Stores infromation relating to updates
    """
    dataset = models.ForeignKey(Dataset, default=5)
    date = models.DateField(default=date.today())
    reason = models.CharField(max_length=100, default='Recurring')
    update_by = models.ManyToManyField(Linker)


class Batch(models.Model):
    """
    Stores information for a new batch for each data set
    """
    FORMATS = (('d', 'del'),
               ('c', 'csv'),
               ('f', 'fixed'),
               ('o', 'other'))
    #I included update although maybe I shouldn't
    TYPE = (('n', 'New'),
            ('c', 'Correction'),
            ('r', 'Refresh'),
            ('o', 'Other'))
    STATUS = (('O','Open'),
              ('C','Closed'),
              ('U','Unassigned'))
    datasetid = models.ForeignKey(Dataset)
    data_recieved = models.DateField()
    batch_type = models.CharField(max_length=6, choices=TYPE)
    #capture date start and end
    data_coverage_start = models.DateField()
    data_coverage_end = models.DateField()
    data_format = models.CharField(max_length=12, choices=FORMATS)
    format_changed = models.BooleanField(default=False)
    #Store hard or soft media
    media = models.CharField(max_length=20)
    person_from = models.ManyToManyField(Client)
    #Path on linkage side usually /raw_data/
    #filepath = models.FilePathField()
    filepath = models.CharField(max_length=20)
    #Only necessary for adhoc
    date_to_destroy = models.DateField()
    # for now check if load profile is needed in future email dev create trac ticket
    new_profile = models.BooleanField(default=False)
    # Related trac ticket number
    trac_ticket = models.IntegerField()
    # Record number of records in and loaded
    recordsin = models.IntegerField()
    recordsloaded = models.IntegerField()
    created_by = models.ManyToManyField(Linker)
    #Want a status field whether batch is open or closed
    status = models.CharField(max_length=12,choices=STATUS,default='U')


    def createdestructiondate(self):
        "Create a destroy date we can use some info to autogenerate this "
        #import datetime
        #if "adhoc" or "non-core":
        #date_to_destroy = datetime.now() + "5 YEARS"
        #Reminder(date,destructioninfo)
        #set a reminder
        pass


class Stage(models.Model):
    '''
    Stores information for each stage of a batch
    '''
    STAGE = (('EV', 'Evaluating'),
             ('CL', 'Cleaning'),
             ('EX', 'Exporting'),
             ('LI', 'Linkage'),
             ('CO','Complete'))
    batchid = models.ForeignKey(Batch)
    startdate = models.DateField()
    starttime = models.TimeField()
    enddate = models.DateField()
    endtime = models.TimeField()
    controller = models.ManyToManyField(Linker)


class HardMedia(models.Model):
    '''
    Capture if it came in on a flash drive , or disk
    '''
    #location where it is stored
    pass


class SoftMedia(models.Model):
    '''
    Want to capture if it came through myft, suffex,email etc
    '''
    pass


class Destruction(models.Model):
    '''
    Store information about what to destroy
    Links, Data, Media, Date etc...
    '''
    pass
