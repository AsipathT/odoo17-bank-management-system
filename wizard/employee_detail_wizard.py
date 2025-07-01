from odoo import models, fields, api

class EmployeeDetailWizard(models.TransientModel):
    _name = 'employee.detail.wizard'
    _description = 'Employee Detail Wizard'

    employee_id = fields.Many2one('bank.employee', string='Employee', required=True)
    detail_notes = fields.Text(string="Detail Notes")
    include_contacts = fields.Boolean(string="Include Contacts")

    def action_print_report(self):
        employee = self.employee_id
        sales = self.env['sale.order'].search([])
        # Build dictionary for report data
        ss=[]
        for sal in sales:
            dat={'name':sal.name,
                 'date':sal.validity_date}
            ss.append(dat)
        data = {
            'employee_id': employee.id,
            'employee_data': {
                'name': employee.name,
                'email': employee.email,
                'phone': employee.phone,
                'department': employee.department,
                'department_code': employee.department_code,
                'employee_code': employee.employee_code,
                'branch_name': employee.branch_id.name if employee.branch_id else '',
                'branch_code': employee.code or '',
                'salary': employee.salary,
                'hire_date': employee.hire_date.strftime('%Y-%m-%d') if employee.hire_date else '',
            },
            'include_contacts': self.include_contacts,
            'detail_notes': self.detail_notes,
            'sales':ss
        }

        return self.env.ref('bank_management_custom.action_report_bank_employee_wizard').report_action(self, data=data)
