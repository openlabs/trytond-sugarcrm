#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .party import *
from .configuration import *


def register():
    "Register classes with pool"
    Pool.register(
        Party,
        Address,
        ContactMechanism,
        Configuration,
        module='sugarcrm', type_='model')
