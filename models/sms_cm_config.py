# -*- coding: utf-8 -*-

import requests

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SmsCmConfig(models.Model):
    _name = 'sms_cm.config'
    _description = _(u'SMS Configuration')

    name = fields.Char(default=_("Unknown"), string=_("Configuration"), required=True, readonly=True, states={'draft':[('readonly',False)]})
    state = fields.Selection([("draft", _("Disabled")), ("done", _("Enabled"))], default="draft", tracking=True, copy=False)
    send_sms_endpoint = fields.Char(required=True, tracking=True, readonly=True, states={'draft':[('readonly',False)]}, help=_("Endpoint for sending SMS"))
    api_sender = fields.Char(required=True, tracking=True, readonly=True, states={'draft':[('readonly',False)]}, help=_("API Sender name")) 
    api_key = fields.Char(required=True, tracking=True, readonly=True, states={'draft':[('readonly',False)]}, help=_("API Key")) 
    api_password = fields.Char(required=True, tracking=True, readonly=True, states={'draft':[('readonly',False)]}, help=_("API Password")) 

    @api.model
    def get_active_config(self):
        allow_custom_sms = self.env['ir.config_parameter'].sudo().get_param('sms_cm.allow_custom_sms') or False
        sms_config = self.search([('state', '=', 'done')], limit=1)

        if allow_custom_sms and not sms_config.exists():
            raise ValidationError(_('We have not found any active SMS configuration.'))
        
        return sms_config

    def action_enable(self):
        active_config = self.search([('state', '=', 'done')])

        if active_config:
            raise ValidationError(_("You already have an active SMS configuration. Please disable the active configuration before continuing."))
            
        for record in self:
            record.state = 'done'

    def action_disable(self):
        for record in self:
            record.state = 'draft'

    @api.model
    def _send_sms_to_number(self, number, message):
        sms_config = self.get_active_config()
        data = {'api_key': sms_config.api_key, 'password': sms_config.api_password, 'sender': sms_config.api_sender, 'phone': number, 'message': message}

        try:
            response = requests.request('POST', url=sms_config.send_sms_endpoint, data=data, auth=False, cert=False, verify=False)
            result = response.json()

            return [{
                'res_id': number,
                'state': result.get('status', 'N/D'),
                'message': result.get('message', 'N/D'),
            }]
        except:
            return [{
                'res_id': number,
                'state': 'error',
                'message': 'API configuration error',
            }]

    @api.model
    def _send_sms(self, numbers, message):
         for number in numbers:
             self._send_sms_to_number(number, message)

    @api.model
    def _send_sms_batch(self, messages):
        """ Send SMS in batch mode

        :param messages: list of SMS to send, structured as dict [{
            'res_id':  integer: ID of sms.sms || phone,
            'phone':  string: E164 formatted phone number,
            'message': string: content to send
        }]

        :return: return of /iap/sms/1/send controller which is a list of dict [{
            'res_id': integer: ID of sms.sms || phone,
            'state':  string: 'error' or 'success',
            'message': response: message
        }]

        :raises: normally none
        """
        result = []
        for message in messages:
            result += [response for response in self._send_sms_to_number(message.get('phone', ''), message.get('message', ''))]
        return result