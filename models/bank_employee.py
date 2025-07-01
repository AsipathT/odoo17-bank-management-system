from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

# Add department model if it does not exist
class BankDepartment(models.Model):
    _name = 'bank.department'
    _description = 'Bank Department'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Department Code')

# Extend bank.employee with department_id and joined_date
class BankEmployee(models.Model):
    _inherit = "bank.employee"

    code = fields.Char("Code", related="branch_id.code", store=True)
    branch_color = fields.Char("Branch Color")
    contact_ids = fields.One2many('bank.contact', 'employee_id', string="Contacts")
    user_id = fields.Many2one('res.users', string='Related User')

    # Add department relation
    department_id = fields.Many2one('bank.department', string='Department')

    # Add joined_date field (date type)
    joined_date = fields.Date(string='Joined Date')

    @api.model
    def create(self, vals):
        if not vals.get('branch_color') and vals.get('branch_id'):
            branch = self.env['bank.branch'].browse(vals['branch_id'])
            vals['branch_color'] = branch.branch_color
        return super().create(vals)

    def action_show_branch_color(self):
        for rec in self:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Branch Color',
                    'message': f"The branch color is: {rec.branch_color or 'Not Set'}",
                    'type': 'info',
                    'sticky': False,
                }
            }

    def action_create_new_contact(self):
        self.ensure_one()
        contact = self.env['bank.contact'].create({
            'name': 'New Contact',
            'employee_id': self.id,
        })
        return {
            'name': 'New Contact',
            'type': 'ir.actions.act_window',
            'res_model': 'bank.contact',
            'view_mode': 'form',
            'res_id': contact.id,
            'target': 'new',
        }

    def action_remove_all_contacts(self):
        self.ensure_one()
        contacts = self.contact_ids
        count = len(contacts)
        if count == 0:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Info',
                    'message': 'No contacts to remove.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        contacts.unlink()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'{count} contact(s) removed.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_edit_first_contact(self):
        self.ensure_one()
        if not self.contact_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Info',
                    'message': 'No contacts to edit.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        contact = self.contact_ids[0]
        return {
            'name': 'Edit Contact',
            'type': 'ir.actions.act_window',
            'res_model': 'bank.contact',
            'view_mode': 'form',
            'res_id': contact.id,
            'target': 'new',
        }

    def action_assign_to_user(self):
        self.ensure_one()
        if not self.user_id:
            raise UserError("Please assign a related user first.")
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'User Assigned',
                'message': f"Employee assigned to user: {self.user_id.name}",
                'type': 'success',
                'sticky': False,
            }
        }

    def action_toggle_branch_color(self):
        self.ensure_one()
        self.branch_color = 'Gold' if self.branch_color != 'Gold' else 'Blue'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Branch Color Changed',
                'message': f"Branch color is now: {self.branch_color}",
                'type': 'info',
                'sticky': False,
            }
        }

    def action_show_employee_summary(self):
        self.ensure_one()
        contact_count = len(self.contact_ids)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Employee Summary',
                'message': f"{self.name} has {contact_count} contact(s).",
                'type': 'info',
                'sticky': False,
            }
        }


# Wizard to print employee detail report
class EmployeeDetailWizard(models.TransientModel):
    _name = 'employee.detail.wizard'
    _description = 'Employee Detail Wizard'

    employee_id = fields.Many2one('bank.employee', string='Employee', required=True)
    detail_notes = fields.Text(string="Detail Notes")
    include_contacts = fields.Boolean(string="Include Contacts")

    def action_print_report(self):
        employee = self.employee_id
        contact_list = []

        if self.include_contacts:
            contact_list = [
                {
                    'name': contact.name,
                    'phone': contact.phone,
                    'email': contact.email,
                    'note': contact.note,
                }
                for contact in employee.contact_ids
            ]

        data = {
            'employee_id': employee.id,
            'employee_name': employee.name,
            'employee_data': {
                'name': employee.name,
                'code': employee.code,
                'email': employee.email,
                'phone': employee.phone,
                'joined_date': employee.joined_date.strftime('%Y-%m-%d') if employee.joined_date else '',
                'branch_color': employee.branch_color,
                'department': {
                    'name': employee.department_id.name if employee.department_id else '',
                    'code': employee.department_id.code or '' if employee.department_id else '',
                },
                'branch': {
                    'id': employee.branch_id.id if employee.branch_id else False,
                    'name': employee.branch_id.name if employee.branch_id else '',
                    'location': employee.branch_id.location or '' if employee.branch_id else '',
                    'manager': employee.branch_id.manager_id.name if employee.branch_id and employee.branch_id.manager_id else '',
                },
                'is_active': employee.active,
                'image_128': employee.image_128,
            },
            'contact_list': contact_list,
            'detail_notes': self.detail_notes,
            'sample_list': ['a', 'b', 'c'],
            'generated_on': datetime.now().strftime('%Y-%m-%d %H:%M'),
        }

        return self.env.ref('bank_management_custom.action_report_bank_employee_wizard').report_action(self, data=data)
