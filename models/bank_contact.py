from odoo import models, fields

class BankContact(models.Model):
    _name = "bank.contact"
    _description = "Bank Contact"

    name = fields.Char(string="Contact Name", required=True)
    employee_id = fields.Many2one('bank.employee', string="Employee")
    phone = fields.Char("Phone")
    mobile = fields.Char("Mobile")
    email = fields.Char("Email")
    address = fields.Char("Address")
