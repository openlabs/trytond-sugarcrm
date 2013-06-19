#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .party import Party, Address, ContactMechanism
from .configuration import Configuration, ImportOpportunitiesWizardView, \
        ImportOpportunitiesWizard


def register():
    "Register classes with pool"
    Pool.register(
        Party,
        Address,
        ContactMechanism,
        Configuration,
        ImportOpportunitiesWizardView,
        module='sugarcrm', type_='model')
    Pool.register(
        ImportOpportunitiesWizard,
        module='sugarcrm', type_='wizard')
