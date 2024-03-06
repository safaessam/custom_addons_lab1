{
    "name": "HMS2",
    "description": "Hospitals Management System",
    "author": "SAFA ESSAM",
    "version": "0.1",
    "category": "Accounting",
    'depends': [
        'base',
        'crm'
    ],
    "data": ["security/res_groups.xml",
                "security/ir.model.access.csv",
                "reports/hms_patient_template.xml",
                "reports/reports.xml",
                "views/hms_patient_view.xml",
                "views/hms_doctor_view.xml", "views/hms_depa_view.xml",
                "views/hms_customer_inherit_view.xml"

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}

