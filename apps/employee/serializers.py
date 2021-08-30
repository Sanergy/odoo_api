from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.Serializer):
    EmployeeGUID = serializers.CharField(required=False, allow_blank=True, max_length=100)
    employee_first_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    employee_last_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    employee_middle_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    employee_full_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    employee_active = serializers.CharField(required=False, allow_blank=True, max_length=100)
    email = serializers.CharField(required=False, allow_blank=True, max_length=100)
    company = serializers.CharField(required=False, allow_blank=True, max_length=100)
    sanergy_department = serializers.CharField(required=False, allow_blank=True, max_length=100)
    departmentName = serializers.CharField(required=False, allow_blank=True, max_length=100)
    sanergy_department_unit = serializers.CharField(required=False, allow_blank=True, max_length=100)
    DepartmentUnit = serializers.CharField(required=False, allow_blank=True, max_length=100)
    employee_role = serializers.CharField(required=False, allow_blank=True, max_length=100)
    primary_phone = serializers.CharField(required=False, allow_blank=True, max_length=100)
    talent_partner_id = serializers.CharField(required=False, allow_blank=True, max_length=100)
    line_manager_id = serializers.CharField(required=False, allow_blank=True, max_length=100)
    TalentPartner = serializers.CharField(required=False, allow_blank=True, max_length=100)
    talent_lead_id = serializers.CharField(required=False, allow_blank=True, max_length=100)
    TeamLead = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        fields = ('employee_first_name', 'employee_last_name')
