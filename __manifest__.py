{
    'name': 'Bank Management Customization',
    'version': '17.0.0.1',
    'summary': 'Managing Bank Employees and Branches using Inheritance',
    'sequence': 0,
    'description': "This app manages details of bank employees and their branches",
    'category': 'Human Resources',
    'website': 'https://www.core48.com',
    'depends': ['base', 'bank_management','sale_management'],
    'data': [
        'security/security.xml',
        'security/employee_record.xml',
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'wizard/employee_detail_wizard_view.xml',  
        'views/bank_employee_views.xml',
        'views/atm_machine_views.xml',
        'views/bank_contact_views.xml',
        'report/report_combined_bank.xml',
        'report/report_action.xml',
        'report/report_bank_employee_template.xml',
        'report/report_bank_employee_wizard_template.xml',
       
         
        

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
