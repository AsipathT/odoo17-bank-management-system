# report_bank_employee.py
from odoo import models

class BankEmployeeReport(models.AbstractModel):
    _name = 'report.bank_management_custom.report_bank_employee_template'  # FIXED
    _description = 'Bank Employee Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['bank.employee'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'bank.employee',
            'docs': docs,
        }
