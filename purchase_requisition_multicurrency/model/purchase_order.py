# -*- coding: utf-8 -*-
#
#
#    Author: Yannick Vaucher
#    Copyright 2014 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.one
    @api.depends('price_unit',
                 'price_subtotal',
                 'order_id.pricelist_id.currency_id',
                 'order_id.requisition_id.date_exchange_rate',
                 'order_id.requisition_id.currency_id')
    def _compute_prices_in_company_currency(self):
        """ """
        requisition = self.order_id.requisition_id
        date = requisition.date_exchange_rate or fields.Date.today()
        from_curr = self.order_id.currency_id.with_context(date=date)
        if requisition and requisition.currency_id:
            to_curr = requisition.currency_id
        else:
            to_curr = self.order_id.company_id.currency_id
        self.price_unit_co = from_curr.compute(self.price_unit,
                                               to_curr, round=False)
        self.price_subtotal_co = from_curr.compute(self.price_subtotal,
                                                   to_curr, round=False)

    @api.multi
    def _requisition_currency(self):
        for rec in self:
            requisition = rec.order_id.requisition_id
            if requisition:
                rec.requisition_currency = requisition.currency_id

    price_unit_co = fields.Float(
        compute='_compute_prices_in_company_currency',
        string="Unit Price",
        digits=dp.get_precision('Account'),
        store=True,
        help="Unit Price in company currency."
        )

    price_subtotal_co = fields.Float(
        compute='_compute_prices_in_company_currency',
        string="Subtotal",
        digits=dp.get_precision('Account'),
        store=True,
        help="Subtotal in company currency."
    )

    order_currency = fields.Many2one(string="Currency", readonly=True,
                                     related="order_id.currency_id")

    requisition_currency = fields.Many2one(
        "res.currency", string="Requisition Currency", readonly=True,
        compute="_requisition_currency")
