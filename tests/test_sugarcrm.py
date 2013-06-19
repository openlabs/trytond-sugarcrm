# -*- coding: utf-8 -*-
"""
    test_sugarcrm

    Test SugarCRM integration with tryton.

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import sugarcrm
import unittest

from mock import patch
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, \
    test_view, test_depends
from trytond.transaction import Transaction
from trytond.config import CONFIG
CONFIG['data_path'] = '.'


class TestSugarCRM(unittest.TestCase):
    """Test SugarCRM Integration.
    """

    def setUp(self):
        trytond.tests.test_tryton.install_module('sugarcrm')
        self.Party = POOL.get('party.party')
        self.PartyAddress = POOL.get('party.address')
        self.SugarcrmConfig = POOL.get('sugarcrm.configuration')
        self.Attachment = POOL.get('ir.attachment')

        self.connection_patcher = patch('sugarcrm.Sugarcrm', autospec=True)
        PatchedConnection = self.connection_patcher.start()
        self.module_patcher = patch('sugarcrm.SugarModule', autospec=True)
        PatchedModule = self.module_patcher.start()
        self.entry_patcher = patch('sugarcrm.SugarEntry', autospec=True)
        PatchedEntry = self.entry_patcher.start()
        connection = sugarcrm.Sugarcrm('Some url', 'admin', 'admin')
        PatchedConnection.return_value.modules = {
            'Opportunities': sugarcrm.SugarModule(
                connection, 'Opportunities'
            ),
            'Accounts': sugarcrm.SugarModule(
                connection, 'Accounts'
            ),
            'Contacts': sugarcrm.SugarModule(
                connection, 'Contacts'
            ),
            'Documents': sugarcrm.SugarModule(
                connection, 'Documents'
            ),
            'EmailAddresses': sugarcrm.SugarModule(
                connection, 'EmailAddresses'
            ),
        }
        PatchedConnection.return_value.get_relationships = \
            lambda *args, **kwargs: {
                'entry_list': []
            }
        PatchedConnection.return_value.modules['Opportunities']._name = \
            'Opportunities'
        PatchedConnection.return_value.modules['Opportunities']._fields = {
            'id': None
        }
        PatchedConnection.return_value.modules['Opportunities']._connection = \
            connection
        PatchedConnection.return_value.modules['Accounts']._name = 'Accounts'
        PatchedConnection.return_value.modules['Contacts']._name = 'Contacts'
        PatchedConnection.return_value.modules['Documents']._name = 'Documents'
        PatchedConnection.return_value.modules['EmailAddresses']._name = \
            'EmailAddresses'
        PatchedConnection.return_value.get_entries_count = lambda x, y: {
            'result_count': '1'
        }
        PatchedModule.return_value = sugarcrm.SugarModule(
            connection, 'Opportunities'
        )
        PatchedModule.return_value._search.return_value = [
            sugarcrm.SugarEntry('Opportunities')
        ]
        values = {
            'id': 'some-ramdom-id',
            'name': 'John Doe'
        }
        PatchedEntry.return_value = sugarcrm.SugarEntry(values)
        PatchedEntry.return_value.__getitem__ = lambda _, field: values[field]
        PatchedEntry.return_value.__setitem__ = lambda _, field, value: True
        PatchedEntry.return_value.get_related = lambda *args, **kwargs: []

    def tearDown(self):
        # Unpatch All patched mocks
        self.connection_patcher.stop()
        self.module_patcher.stop()
        self.entry_patcher.stop()

    def test0005views(self):
        '''
        Test views.
        '''
        test_view('sugarcrm')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()

    def setup_defaults(self):
        "Setup defaults"
        self.SugarcrmConfig.write([1], {
            'url': 'Some URL',
            'username': 'admin',
            'password': 'admin'
        })

    def test_0010_fetch_opportunities(self):
        """Test the fetching of opportunities from sugarcrm
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            # Call method to setup defaults
            self.setup_defaults()

            self.assertEqual(len(self.Party.search([])), 0)
            self.assertEqual(len(self.PartyAddress.search([])), 0)

            self.Party.import_opportunities_from_sugarcrm()
            self.assertTrue(len(self.Party.search([])) > 0)
            self.assertTrue(len(self.PartyAddress.search([])) > 0)


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSugarCRM))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
