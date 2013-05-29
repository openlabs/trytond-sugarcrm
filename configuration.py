# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import sugarcrm

from trytond.wizard import Wizard, StateView, Button
from trytond.model import ModelSingleton, ModelSQL, ModelView, fields
from trytond.pool import Pool


__all__ = [
    'Configuration', 'ImportOpportunitiesWizardView',
    'ImportOpportunitiesWizard'
]


class Configuration(ModelSingleton, ModelSQL, ModelView):
    "SugarCRM Configuration"
    __name__ = 'sugarcrm.configuration'

    last_import_time = fields.DateTime('Last import time')
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
        cls._buttons.update({
            'test_connection': {},
            'import_opportunities': {},
        })

    def get_sugarcrm_connection(self):
        """
        Returns an authenticated instance of the SugarCRM client

        :return: SugarCRM connection object
        """
        if not all([self.url, self.username, self.password]):
            self.raise_user_error('sugarcrm_settings_missing')

        return sugarcrm.Sugarcrm(self.url, self.username, self.password)

    @ModelView.button
    def test_connection(self):
        """Test SugarCRM connection and display appropriate message to user
        """
        try:
            self.get_sugarcrm_connection()
        except ValueError, exc:
            self.raise_user_error(
                'Connection Failed. Please check the REST API URL!'
            )
        except sugarcrm.SugarError, exc:
            self.raise_user_error(
                'Connection Failed. Incorrect username and/or password!'
            )

        self.raise_user_error('Connection Successful.')

    @classmethod
    @ModelView.button_action('sugarcrm.wizard_import_opportunity')
    def import_opportunities(cls, configurations):
        """Import opportunities from SugarCRM

        :param configurations: List of records
        """
        pass


class ImportOpportunitiesWizardView(ModelView):
    'Import Opportunities Wizard View'
    __name__ = 'import.sugar.opportunities.wiz.view'


class ImportOpportunitiesWizard(Wizard):
    'Import Opportunities Wizard'
    __name__ = 'import.sugar.opportunities.wiz'

    start = StateView(
        'import.sugar.opportunities.wiz.view',
        'sugarcrm.import_sugar_opportunities_wiz_view_form',
        [
            Button('Ok', 'end', 'tryton-ok'),
        ]
    )

    def default_start(self, data):
        """Import the opportunities and display a confirmation message
        to the user

        :param data: Wizard data
        """
        Party = Pool().get('party.party')

        Party.import_opportunities_from_sugarcrm()

        return {}
