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
import types
from zope import interface, component
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.security.proxy import removeSecurityProxy
from zope.app.intid.interfaces import IIntIds
from zope.app.container.interfaces import IObjectMovedEvent
from zope.app.container.contained import notifyContainerModified

from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IOrder, IReordable

from interfaces import ISorting


class Order(object):
    interface.implements(IOrder)

    def __init__(self, context):
        self.context = context
        self.sorting = ISorting(context)
        self.results = self.sorting.getItems()

    def addItem(self, name):
        self.sorting.addItem(name)

    def removeItem(self, name):
        self.sorting.removeItem(name)

    def keys(self):
        return range(len(self.results))

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return iter(range(len(self.results)))

    def __getitem__(self, key):
        return self.results[key]

    def get(self, key, default=None):
        return self.results.get(key, default)

    def values(self):
        return list(self.results)

    def items(self):
        results = self.results
        return [(idx, results[idx]) for idx in range(len(self.results))]

    def __contains__(self, key):
        return (key >=0) and (key < len(self.results))

    has_key = __contains__
