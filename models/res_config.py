# -*- coding: utf-8 -*-

from odoo import fields, models, api



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_custom_sms = fields.Boolean(
        string='SMS custom provider', 
        help='Use custom provider to send SMS. Override IAP SMS.',
        config_parameter='sms_cm.allow_custom_sms'
    )

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('sms_cm.allow_custom_sms', self.allow_custom_sms)

        return res
        
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update({'allow_custom_sms': params.get_param('sms_cm.allow_custom_sms') or False})

        return res
