
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import CustomUser

class Employee(models.Model):
    id = models.CharField(primary_key=True,max_length=100, blank=False)
    sf_user_id = models.CharField(max_length=100, blank=True, null=True)
    employee_first_name = models.CharField(max_length=100, blank=False, null=True)
    employee_first_name = models.CharField(max_length=100, blank=False, null=True)
    employee_last_name = models.CharField(max_length=100, null=True)
    employee_middle_name = models.CharField(max_length=100, null=True)
    employee_full_name = models.CharField(max_length=100, blank=False)
    sanergy_department = models.CharField(max_length=100, blank=False, null=True)
    sanergy_department_unit=models.ForeignKey('leave_management.SanergyDepartmentUnit', on_delete=models.DO_NOTHING, null=True)
    employee_active = models.BooleanField(default=True, null=True)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    isdeleted = models.BooleanField(null=True)
    image = models.FileField(default='default.jpg', upload_to='profile_pics')
    date_of_birth = models.DateField(default=timezone.now)
    joined_date = models.DateField(default=timezone.now)
    is_staff = models.BooleanField(default=False, null=True)
    is_employee = models.BooleanField(default=True, null=True)
    hr_employee_id = models.CharField(unique=True, max_length=100, null=True)
    leave_group = models.CharField(unique=False, max_length=100, null=True)
    employee_role = models.CharField(unique=False, max_length=100, null=True)
    primary_phone = models.CharField(max_length=100, blank=True, null=True)
    hr_unique_record_id = models.CharField(max_length=100, blank=True, null=True)
    # user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null = True, blank=True)
    
    team_lead = models.ForeignKey('Employee', on_delete=models.DO_NOTHING, null=True, related_name='employee_team_lead')
    line_manager = models.ForeignKey('Employee', on_delete=models.DO_NOTHING, null=True, related_name='employee_line_manager')
    talent_partner = models.ForeignKey('Employee', on_delete=models.DO_NOTHING, null=True, related_name='employee_talent_partner')

    class Meta:
        managed = True
        db_table = 'employee_employee'
        ordering = ('employee_first_name',)

    def __str__(self):
        return self.employee_full_name

    def __repr__(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.pk})

class EmployeeView():
    class Meta:
        ordering = ('employee_first_name',)

    def __str__(self):
        return self.employee_full_name

    def __repr__(self):
        return self.__str__()


class EmployeeRole(models.Model):
    id = models.CharField(primary_key=True,max_length=100, blank=False)
    role_code = models.CharField(max_length=100, null=True)
    job_title = models.CharField(max_length=100, blank=False, null=True)
    reg_mapping = models.TextField(max_length=10000, null=True)
    reg_manager_mapping = models.TextField(max_length=10000, null=True)
    department_unit = models.TextField(max_length=10000, null=True)
    line_manager = models.TextField(max_length=10000, null=True)
    role_name = models.TextField(max_length=10000, null=True)

    def __int__(self):
        return self.id




