# -*- coding: utf-8 -*-
{
    'name': "SMS CM",

    'summary': """
        Send SMS to your contacts.""",

    'description': """
    """,

    'author': "Parfait BENE",
    'website': "https://parfaitbene.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Email Marketing',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mass_mailing_sms'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_config_views.xml',
        'views/sms_cm_config.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
