# -*- coding: utf-8 -*-

{
    'name': 'HMS',
    'summary': 'Hospitals Management System',
    'author': 'Safa Essam',
    'version': '1.0',
    'depends': ['base'],
    'category' : 'sales',
    'data': [
        'security/ir.model.access.csv',
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctor_views.xml',
    ],
     'installable': True,
     'application': True,


}