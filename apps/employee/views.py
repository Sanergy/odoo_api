from django.shortcuts import render
import xmlrpc.client
from odooapi import settings
from django.utils import timezone
import json,csv,logging,datetime,locale
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse 
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(['GET'])
def index(request):    
    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))
    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})

    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))
    records = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'fields_get',[], {'attributes': ['string', 'help', 'type']})

    #return JsonResponse(records, safe=False)
    return Response(data=records, status=status.HTTP_200_OK)

@api_view(['GET'])
def records(request):    
    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))
    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})

    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))
    
    record  = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'search_read', 
                [[['newly_hired_employee', '=', True]]],  {'fields': 
                ['name','gender','job_title','department_id','work_email','mobile_phone','work_location','marital','parent_id','category_ids','job_id','newly_hired_employee','create_date','active']
            })
    
    return Response(data=record, status=status.HTTP_200_OK)

@api_view(['GET'])
def post(request):
    data    = json.loads(request.body.decode("utf-8"))
    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))
    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})

    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))
    id      = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'create', [{
                    'name': data['name'],
                    'gender': data['gender'],
                    'work_email': data['work_email'],
                    'mobile_phone': data['mobile_phone'],
                    'work_location': data['work_location'],
                    'marital': data['marital'],
                    'newly_hired_employee': data['newly_hired_employee'],
                    'department_id': data['department_id'],
                    'job_id': data['job_id'],
                    'parent_id': data['parent_id'],
                    'category_ids': data['category_ids'],
                }])

    # get record name after having posting it
    record  = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'name_get', [[id]])
    
    return Response(data=record, status=status.HTTP_200_OK)

@api_view(['GET'])
def update(request):
    data    = json.loads(request.body.decode("utf-8"))

    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))
    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})
    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))

    models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'write', [[data['id']], {
                    'name': data['name'],
                    'gender': data['gender'],
                    'work_email': data['work_email'],
                    'mobile_phone': data['mobile_phone'],
                    'work_location': data['work_location'],
                    'marital': data['marital'],
                    'newly_hired_employee': data['newly_hired_employee'],
                    'department_id': data['department_id'],
                    'job_id': data['job_id'],
                    'parent_id': data['parent_id'],
                    'category_ids': data['category_ids'],
                }])
    # get record name after having changed it
    record  = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'name_get', [[data['id']]])
    
    return Response(data=record, status=status.HTTP_200_OK)

def sync():
    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))
    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})

    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))
    record  = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 
                'hr.employee', 'search_read', [[['active', '=', True],['newly_hired_employee','=',True]]],  
                {'fields': ['name','gender','job_title','department_id','work_email','mobile_phone','work_location','marital','parent_id','category_ids','job_id','newly_hired_employee','create_date','active']}
            )

    for item in record:
        #print(str(timezone.now())+' Posting: ',item['id'])
        logger.info(str(timezone.now())+'Processing employee id: '+str(item['id']))
        
        #check if record exists
        check = Employee.objects.filter(email=item['work_email']).count()
        if check == 0:
            #post new record to db
            employee = Employee()
            employee.sf_user_id = item['id']
            employee.email = item['work_email']
            employee.primary_phone = item['mobile_phone']
            employee.save()

            logger.info(str(timezone.now())+'Added employee id: '+str(item['id']))
        else:
            #update
            Employee.objects.filter(email=item['work_email']).update(
                    primary_phone=item['mobile_phone']
            )

            logger.info(str(timezone.now())+'Updating employee id: '+str(item['id']))

    return JsonResponse(record, safe=False)
