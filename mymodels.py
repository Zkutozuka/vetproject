from peewee import *

database = PostgresqlDatabase('vetclinic', **{'user': 'vetman'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Dogowners(BaseModel):
    address = CharField()
    ownerfirstname = CharField()
    ownerid = AutoField()
    ownerlastname = CharField()
    phonenumber = CharField()

    class Meta:
        table_name = 'dogowners'

class Dogs(BaseModel):
    breed = CharField()
    chipnumber = IntegerField(null=True)
    dateofbirth = DateField()
    dogid = AutoField()
    dogname = CharField()
    knownallergies = CharField(null=True)
    lastvaccinationdate = DateField()
    ownerid = IntegerField()
    petinsurancedetails = CharField(null=True)

    class Meta:
        table_name = 'dogs'

class Vaccination(BaseModel):
    date = DateField()
    dogid = IntegerField()
    staffid = IntegerField()
    vaccinationid = AutoField()
    vaccinecode = CharField()

    class Meta:
        table_name = 'vaccination'

class Vaccines(BaseModel):
    description = CharField()
    vaccinecode = CharField(primary_key=True)

    class Meta:
        table_name = 'vaccines'

class Vetstaff(BaseModel):
    address = CharField()
    daysoff = CharField()
    firstname = CharField()
    lastname = CharField()
    phonenumber = CharField()
    staffid = AutoField()
    title = CharField()

    class Meta:
        table_name = 'vetstaff'

class Visits(BaseModel):
    dateofvisit = DateField()
    dogid = IntegerField()
    followupdate = DateField(null=True)
    insuranceclaim = CharField(null=True)
    medprescription = CharField(null=True)
    problem = CharField()
    staffid = IntegerField()
    totalbill = CharField()
    visitid = AutoField()

    class Meta:
        table_name = 'visits'

