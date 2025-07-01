from odoo import models, fields

class AtmMachine(models.Model):
    _inherit = "bank.atm"

    code = fields.Char("Code", related="branch_id.code", store=True)
    #branch_color = fields.Char("Branch Color", related="branch_id.branch_color", store=True)
