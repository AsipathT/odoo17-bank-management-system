from odoo import models

class ReportCombinedBank(models.AbstractModel):
    _name = 'report.bank_management_custom.report_combined_bank_template'
    _description = 'Combined Bank Employee Report with Sales Data'

    def _get_report_values(self, docids, data=None):
        employees = self.env['bank.employee'].browse(docids)
        results = []
        print(employees)
        for emp in employees:
            partner = self.env['res.partner'].search([('name', 'ilike', emp.name)], limit=1)
            print(partner)
            sales_orders = self.env['sale.order'].search([('partner_id', '=', partner.id)]) if partner else []
            print(sales_orders)
            
            results.append({
                'employee': emp,
                'sales_orders': sales_orders,
            })

        return {
            'docs': employees,
            'results': results,
        }
