# -*- coding: utf-8 -*-
{
    'name': "To Doo app",
    'summary': "",
    'description': "an todo app ",
    'author': "Safa Essam",
    'category': 'Marketing',
    'version': '17.0.0.1.0',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/ticket_tree_view.xml',
        'views/ticket_kanban_view.xml',
        'views/ticket_form_view.xml',
        'views/todo_action.xml',
        'views/base_menus.xml',
    ],
}
