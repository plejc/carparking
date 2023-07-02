from typing import Any
from django.db import models
from uuid import uuid4






class Employee(models.Model): #A
    ''' employee table according to his/her expertise of doamin.'''
    expertise_enum = (
        ("Debit",'Debit'),
        ("Loans","Loans"),
        ("Demat","Demat"),
        ("Insurance","Insurance"),
        ("Account","Account")
    )
    uid = models.UUIDField(primary_key=True ,default=uuid4, editable=False)
    first_name = models.CharField("first name", blank=False, null=False, max_length=50)
    last_name = models.CharField("last-name", blank=True, null=True, max_length=50)
    email = models.EmailField("email", unique=True, error_messages={"unique":"An email is already registered"})
    exprtise = models.CharField("expertise-in", choices=expertise_enum,max_length=10,blank=False, null=False)
    phone = models.BigIntegerField("phone")

    def __str__(self):
        return self.first_name
    
class CustomerQuery(models.Model): #B
    ''' model to store customer complain'''
    query_enum = (
        ("Debit",'Debit'),
        ("Loans","Loans"),
        ("Demat","Demat"),
        ("Insurance","Insurance"),
        ("Account","Account")
    )
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    query_type = models.CharField("query-type", choices=query_enum, max_length=10, blank=False, null=False)
    first_name = models.CharField("first name", blank=False, null=False, max_length=50)
    last_name = models.CharField("last name", blank=False, null=False,max_length=50)
    email = models.EmailField("customer-email", blank=False, null=False)
    raised_on =  models.DateField("raised date", blank=False, null=False)
    resolved_on = models.DateField("resolved date", blank=True, null=True)
    resolved_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    query_status = models.BooleanField()

    def __str__(self):
        return self.query_type
    

class EmployeeExpertise(models.Model):
    '''employee expertise'''
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    expertise = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.DO_NOTHING)
    domain_experiance = models.IntegerField()

    def __str__(self):
        return self.expertise.first_name
    
class QueryAssignedEmployee(models.Model):
    '''model to store number of query assigned to employeee to resolved weekly/monthly/yearly'''
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    assigned_query = models.IntegerField()
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    task_status = models.BooleanField()

    def __str__(self):
        return self.employee.first_name

class EmployeePerformanceReport(models.Model):
    ''' assesement of employee weekly/monthly/yearly'''
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    performance_report = models.DecimalField(max_digits=5, decimal_places=2)
    query_assigned = models.ManyToManyField(QueryAssignedEmployee)
    def __str__(self):
        return self.uid
    




