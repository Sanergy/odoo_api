from django.shortcuts import render
import json
import xmlrpc.client
from odooapi import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse 


def index(request):    
    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))
    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})

    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))
    records = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'fields_get',[], {'attributes': ['string', 'help', 'type']})

    return JsonResponse(records, safe=False)

def records(request):    
    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))
    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})

    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))
    ids     = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'search', [[]])
    record  = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'read', [ids], {'fields': ['name','gender','job_title','department_id','work_email','mobile_phone','work_location','marital','newly_hired_employee','create_date','active']})
    
    return JsonResponse(record, safe=False)


def post(request):
    data    = json.loads(request.body.decode("utf-8"))
    print(data)
    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))
    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})

    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))
    id      = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'create', [{
                'name': "New Employee 1",
            }])

    # get record name after having posting it
    record  = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'name_get', [[id]])
    
    return JsonResponse(record, safe=False)

def update(request):
    common  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_URL))

    uid     = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {})
    models  = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_URL))

    models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'write', [[20], {
                    'name': "Jeniffer Abigail"
                }])
    # get record name after having changed it
    record  = models.execute_kw(settings.ODOO_DB, uid, settings.ODOO_PASSWORD, 'hr.employee', 'name_get', [[20]])
    
    return JsonResponse(record, safe=False)



