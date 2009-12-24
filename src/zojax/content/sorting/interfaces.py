##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.content.sorting')


class ISortable(interface.Interface):
    """marker interface for sortable container"""


class ISortingType(interface.Interface):
    """Sorting type"""

    title = interface.Attribute('Title')

    description = interface.Attribute('Description')

    def generateKey(content):
        """ gerentate float sort key """


class ISorting(interface.Interface):
    """Container contents sorting extension."""

    type = schema.Choice(
        title = _(u'Sort type'),
        description = _(u'Select sorting method.'),
        vocabulary = 'content.sorting-types',
        default = u'name',
        required = True)

    order = schema.Choice(
        title = u'Sort order',
        values = ['direct', 'reverse'],
        default = 'direct',
        required = True)

    index = interface.Attribute('Index')
    mapping = interface.Attribute('Mapping')

    def getItems():
        """return ordered items"""

    def addItem(name):
        """ add item to index """

    def updateItem(name):
        """ update item """

    def removeItem(name):
        """ remove item to index """

    def rebuild():
        """ rebuild index """
