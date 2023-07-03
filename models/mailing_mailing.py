# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _

class Mailing(models.Model):
    _inherit = 'mailing.mailing'

    @api.depends('mailing_trace_ids.failure_type')
    def _compute_sms_has_iap_failure(self):
        for mail in self:
            mail.sms_has_insufficient_credit = False
            mail.sms_has_unregistered_account = False


