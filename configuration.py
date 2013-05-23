# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import sugarcrm
from trytond.model import ModelSingleton, ModelSQL, ModelView, fields


__all__ = ['Configuration']


class Configuration(ModelSingleton, ModelSQL, ModelView):
    "SugarCRM Configuration"
    __name__ = 'sugarcrm.configuration'

    last_import_time = fields.DateTime('SugarCRM last import time')
    url = fields.Property(
        fields.Char('REST API URL', required=True)
    )
    username = fields.Property(
        fields.Char('Username', required=True)
    )
    password = fields.Property(
        fields.Char('Password', required=True)
    )

    @classmethod
    def __setup__(cls):
        super(Configuration, cls).__setup__()
        cls._error_messages.update({
            'sugarcrm_settings_missing': \
                'SugarCRM settings on company are incomplete.',
        })

    def get_sugarcrm_connection(self):
        """
        Returns an authenticated instance of the SugarCRM client

        :return: SugarCRM connection object
        """
        if not all([self.url, self.username, self.password]):
            self.raise_user_error('sugarcrm_settings_missing')

        return sugarcrm.Sugarcrm(self.url, self.username, self.password)
