# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import base64
from datetime import datetime

from sugarcrm import QueryList, SugarEntry

from trytond.model import fields
from trytond.pool import PoolMeta, Pool

__all__ = ['Party', 'Address', 'ContactMechanism']
__metaclass__ = PoolMeta


class ContactMechanism:
    "Contact Mechanism"
    __name__ = 'party.contact_mechanism'

    @classmethod
    def create_from_sugarcrm_account(cls, account, party, connection=None):
        """Create contact mechanisms for the given party from the
        sugarcrm account provided.

        ..note:: The account here refers to the customer account from
            sugarcrm `Accounts` module

        :param account: SugarCRM Account instance
        :param party: Party active record

        :returns: A list of contact mechanisms created
        """
        Configuration = Pool().get('sugarcrm.configuration')

        contact_mechanisms = []

        for contact_type in [
                'phone_office', 'phone_alternate', 'website'
            ]:
            if not account[contact_type]:
                continue
            contact_mechanisms.append(
                cls.create({
                    'type': contact_type.split('_')[0],
                    'value': account[contact_type],
                    'party': party.id,
                })
            )
            if account['phone_fax']:
                contact_mechanisms.append(
                    cls.create({
                        'type': 'fax',
                        'value': account['phone_fax'],
                        'party': party.id,
                    })
                )

        if not connection:
            connection = Configuration(1).get_sugarcrm_connection()
        # Get email addresses
        emails = account.get_related(connection.modules['EmailAddresses'])

        for email in emails:
            contact_mechanisms.append(
                cls.create({
                    'type': 'email',
                    'value': email['email_address'],
                    'party': party.id,
                })
            )
        return contact_mechanisms

    @classmethod
    def create_from_sugarcrm_contact(cls, contact, party, connection=None):
        """Create contact mechanisms for the given party from the
        sugarcrm contact provided.

        ..note: The contact here refers to the customer contact from
            sugarcrm `Contacts` module

        :param contact: SugarCRM Contact instance
        :param party: Party active record

        :returns: A list of contact mechanisms created
        """
        Configuration = Pool().get('sugarcrm.configuration')

        contact_mechanisms = []

        for contact_type in [
                'phone_home', 'phone_work', 'phone_other'
            ]:
            if not contact[contact_type]:
                continue
            contact_mechanisms.append(
                cls.create({
                    'type': contact_type.split('_')[0],
                    'value': contact[contact_type],
                    'party': party.id,
                })
            )
            if contact['phone_fax']:
                contact_mechanisms.append(
                    cls.create({
                        'type': 'fax',
                        'value': contact['phone_fax'],
                        'party': party.id,
                    })
                )
            if contact['phone_mobile']:
                contact_mechanisms.append(
                    cls.create({
                        'type': 'mobile',
                        'value': contact['phone_mobile'],
                        'party': party.id,
                    })
                )

        if not connection:
            connection = Configuration(1).get_sugarcrm_connection()
        # Get email addresses
        emails = contact.get_related(connection.modules['EmailAddresses'])

        for email in emails:
            contact_mechanisms.append(
                cls.create({
                    'type': 'email',
                    'value': email['email_address'],
                    'party': party.id,
                })
            )
        return contact_mechanisms


class Address:
    "Address"
    __name__ = 'party.address'

    sugarcrm_id = fields.Char('SugarCRM ID', readonly=True)

    @classmethod
    def create_from_sugarcrm_account(cls, account, party):
        """Create addresses for the given party from the
        sugarcrm account provided.

        ..note: The account here refers to the customer account from
            sugarcrm `Accounts` module

        :param account: SugarCRM Account instance
        :param party: Party active record

        :returns: A list of addresses created
        """
        Country = Pool().get('country.country')
        Subdivision = Pool().get('country.subdivision')

        addresses = []

        billing_country = Country.search([
            ('name', 'ilike', account['billing_address_country'])
        ], limit=1) or None
        billing_state = Subdivision.search([
            ('name', 'ilike', account['billing_address_state']),
            ('country', '=', billing_country[0].id)
        ], limit=1) if billing_country else None

        # Create address only if street, city or postal code exist
        if any([
                account['billing_address_street'],
                account['billing_address_city'],
                account['billing_address_postalcode']
            ]):
            addresses.append(cls.create(
                {
                    'name': account['name'],
                    'street': account['billing_address_street'],
                    'city': account['billing_address_city'],
                    'zip': account['billing_address_postalcode'],
                    'subdivision': billing_state and billing_state[0].id,
                    'country': billing_country and billing_country[0].id,
                    'sugarcrm_id': account['id'],
                    'party': party.id,
                }
            ))
        shipping_country = Country.search([
            ('name', 'ilike', account['shipping_address_country'])
        ], limit=1) or None
        shipping_state = Subdivision.search([
            ('name', 'ilike', account['shipping_address_state']),
            ('country', '=', shipping_country[0].id)
        ], limit=1) if shipping_country else None

        # Create address only if street, city or postal code exist
        if any([
                account['shipping_address_street'],
                account['shipping_address_city'],
                account['shipping_address_postalcode']
            ]):
            addresses.append(cls.create(
                {
                    'name': account['name'],
                    'street': account['shipping_address_street'],
                    'city': account['shipping_address_city'],
                    'zip': account['shipping_address_postalcode'],
                    'subdivision': shipping_state and shipping_state[0].id,
                    'country': shipping_country and shipping_country[0].id,
                    'sugarcrm_id': account['id'],
                    'party': party.id,
                }
            ))

        return addresses

    @classmethod
    def create_from_sugarcrm_contact(cls, contact, party):
        """Create addresses for the given party from the
        sugarcrm contact provided.

        ..note: The contact here refers to the customer account from
            sugarcrm `Contacts` module

        :param contact: SugarCRM Contact instance
        :param party: Party active record

        :returns: A list of addresses created
        """
        Country = Pool().get('country.country')
        Subdivision = Pool().get('country.subdivision')

        addresses = []

        primary_country = Country.search([
            ('name', 'ilike', contact['primary_address_country'])
        ], limit=1) or None
        primary_state = Subdivision.search([
            ('name', 'ilike', contact['primary_address_state']),
            ('country', '=', primary_country[0].id)
        ], limit=1) if primary_country else None

        # Create address only if street, city or postal code exist
        if any([
                contact['primary_address_street'],
                contact['primary_address_city'],
                contact['primary_address_postalcode']
            ]):
            addresses.append(cls.create(
                {
                    'name': contact['name'],
                    'street': contact['primary_address_street'],
                    'city': contact['primary_address_city'],
                    'zip': contact['primary_address_postalcode'],
                    'subdivision': primary_state and primary_state[0].id,
                    'country': primary_country and primary_country[0].id,
                    'sugarcrm_id': contact['id'],
                    'party': party.id,
                }
            ))
        alt_country = Country.search([
            ('name', 'ilike', contact['alt_address_country'])
        ], limit=1) or None
        alt_state = Subdivision.search([
            ('name', 'ilike', contact['alt_address_state']),
            ('country', '=', alt_country[0].id)
        ], limit=1) if alt_country else None

        # Create address only if street, city or postal code exist
        if any([
                contact['primary_address_street'],
                contact['primary_address_city'],
                contact['primary_address_postalcode']
            ]):
            addresses.append(cls.create(
                {
                    'name': contact['name'],
                    'street': contact['alt_address_street'],
                    'city': contact['alt_address_city'],
                    'zip': contact['alt_address_postalcode'],
                    'subdivision': alt_state and alt_state[0].id,
                    'country': alt_country and alt_country[0].id,
                    'sugarcrm_id': contact['id'],
                    'party': party.id,
                }
            ))

        return addresses


class Party:
    "Party"
    __name__ = 'party.party'

    sugarcrm_id = fields.Char('SugarCRM Reference', readonly=True)

    @classmethod
    def __setup__(cls):
        "Setup"
        super(Party, cls).__setup__()
        cls._error_messages.update({
            'sugarcrm_id_not_found': \
                'This Party is not linked to a SugarCRM opportunity'
        })

    @classmethod
    def create_from_sugarcrm(cls, opportunity, connection=None):
        """
        Create  a party and addresses from the SugarCRM opportunity record

        :param connection: SugarCRM connection instance
        :param opportunity: SugarCRM opportunity object
        """
        Address = Pool().get('party.address')
        ContactMechanism = Pool().get('party.contact_mechanism')
        Configuration = Pool().get('sugarcrm.configuration')

        # Check if this opportunity already exists in tryton
        existing_party = cls.search([
            ('sugarcrm_id', '=', opportunity['id'])
        ])
        if existing_party:
            # TODO: Update some details too
            return

        if not connection:
            connection = Configuration(1).get_sugarcrm_connection()

        party = cls.create({
            'name': opportunity['name'],
            'sugarcrm_id': opportunity['id'],
        })

        account_module = connection.modules['Accounts']
        contact_module = connection.modules['Contacts']

        related_account_ids = opportunity.get_related(account_module)
        if related_account_ids:
            query_account = QueryList(account_module)._build_query(
                id__in=[a['id'] for a in related_account_ids]
            )
            # Fetch the required fields for all these account to make the
            # process faster
            related_accounts = account_module._search(
                query_account, fields=[
                    'name', 'billing_address_street', 'billing_address_city',
                    'billing_address_state', 'billing_address_postalcode',
                    'billing_address_country', 'shipping_address_street',
                    'shipping_address_city', 'shipping_address_state',
                    'shipping_address_postalcode', 'shipping_address_country',
                    'phone_fax', 'phone_office', 'phone_alternate', 'website',
                ]
            )

            # Create addresses for all accounts linked to opportunity
            # Ideally it should be only one with a billing and a shipping
            # address
            for account in related_accounts:
                Address.create_from_sugarcrm_account(account, party)
                ContactMechanism.create_from_sugarcrm_account(
                    account, party, connection
                )

        related_contact_ids = opportunity.get_related(contact_module)
        if related_contact_ids:
            query_contact = QueryList(contact_module)._build_query(
                id__in=[a['id'] for a in related_contact_ids]
            )
            # Fetch the required fields for all these account to make the
            # process faster
            related_contacts = contact_module._search(
                query_contact, fields=[
                    'first_name', 'last_name', 'primary_address_street',
                    'primary_address_city', 'primary_address_state',
                    'primary_address_postalcode', 'primary_address_country',
                    'alt_address_street', 'alt_address_city',
                    'alt_address_state', 'alt_address_postalcode',
                    'alt_address_country', 'phone_fax', 'phone_home',
                    'phone_mobile', 'phone_work', 'phone_other'
                ]
            )

            # Create addresses for all contacts linked to opportunity
            for contact in related_contacts:
                Address.create_from_sugarcrm_contact(contact, party)
                ContactMechanism.create_from_sugarcrm_contact(
                    contact, party, connection
                )

        # Fetch the documents attached to this opportunity
        party.fetch_documents_from_sugarcrm()

        return party

    def fetch_documents_from_sugarcrm(self):
        """Fetch the documents attached to the given party's opportunity
        from SugarCRM and its Accounts and Contacts
        """
        Configuration = Pool().get('sugarcrm.configuration')
        Attachment = Pool().get('ir.attachment')

        if not self.sugarcrm_id:
            self.raise_user_error('sugarcrm_id_not_found')

        connection = Configuration(1).get_sugarcrm_connection()
        account_module = connection.modules['Accounts']
        contact_module = connection.modules['Contacts']
        document_module = connection.modules['Documents']

        # Create the Opportunity record from the party's sugarcrm_id
        opportunity = SugarEntry(connection.modules['Opportunities'])
        opportunity['id'] = self.sugarcrm_id

        # Get related accounts and contacts for this opportunity
        related_accounts = opportunity.get_related(account_module)
        related_contacts = opportunity.get_related(contact_module)

        # Fetch the related documents to this opportunity and its related
        # accounts and contacts
        documents = opportunity.get_related(document_module)
        for account in related_accounts:
            documents.extend(account.get_related(document_module))
        for contact in related_contacts:
            documents.extend(contact.get_related(document_module))

        for doc in documents:
            doc_data = connection.get_document_revision(
                doc['document_revision_id']
            )
            Attachment.create({
                'name': doc_data['document_revision']['filename'],
                'type': 'data',
                'data': buffer(base64.decodestring(
                    doc_data['document_revision']['file']
                )),
                'resource': '%s,%s' % (self.__name__, self.id)
            })

    @classmethod
    def import_opportunities_from_sugarcrm(cls):
        """Import Opportunities from SugarCRM
        """
        Configuration = Pool().get('sugarcrm.configuration')

        last_import_time = Configuration(1).last_import_time

        connection = Configuration(1).get_sugarcrm_connection()
        opportunity_module = connection.modules['Opportunities']

        # If this is the first import then there is no last_import_time
        # Hence we should import all opportunities which are created
        # till now
        if not last_import_time:
            query = QueryList(opportunity_module)._build_query(
                sales_stage__exact='Closed Won'
            )
        else:
            query = QueryList(opportunity_module)._build_query(
                date_updated__gt=last_import_time,
                sales_stage__exact='Closed Won'
            )

        total_opportunities_to_fetch = int(connection.get_entries_count(
            'Opportunities', query
        )['result_count'] or 0)

        if not total_opportunities_to_fetch:
            return

        Configuration.write([Configuration(1)], {
            'last_import_time': datetime.utcnow()
        })

        # Paginate the records for 100 count on each call
        for i in range(0, total_opportunities_to_fetch, 100):
            opportunities = opportunity_module._search(
                query, start=i, total=i+100, fields=['name']
            )

            for opportunity in opportunities:
                cls.create_from_sugarcrm(opportunity, connection)
