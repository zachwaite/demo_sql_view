import odoo
from odoo import fields, models


class CustomerSalesViewmodel(models.Model):
    _name = "customer.sales.viewmodel"
    _description = "CustomerSalesViewmodel"
    _auto = False
    _order = "total_sales DESC"

    id = fields.Integer(readonly=True)
    customer_name = fields.Char(readonly=True)
    total_sales = fields.Float(readonly=True)

    @property
    def _query(self):
        return """
SELECT
       ROW_NUMBER() OVER (ORDER BY customers.id) AS id,
       customers.name AS customer_name,
       SUM(sales.amount_total) AS total_sales
FROM
     res_partner AS customers,
     sale_order AS sales
WHERE
    sales.partner_id = customers.id
GROUP BY 
    customers.id
        """

    def init(self):
        odoo.tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query)
        )
