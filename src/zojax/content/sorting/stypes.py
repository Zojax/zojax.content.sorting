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
import time
from pytz import utc
from datetime import datetime
from zope import interface
from zope.dublincore.interfaces import IDCTimes, IDCDescriptiveProperties
from zojax.content.sorting.interfaces import _, ISortingType


class SortByName(object):
    interface.implements(ISortingType)

    title = _(u'Sort by name')
    description = u''

    def value(self, content):
        return content.__name__


class SortByTitle(object):
    interface.implements(ISortingType)

    title = _(u'Sort by title')
    description = u''

    def value(self, content):
        return IDCDescriptiveProperties(content).title


class SortByModified(object):
    interface.implements(ISortingType)

    title = _(u'Sort by modification time')
    description = u''
    default = datetime(2000, 1, 1, tzinfo=utc)

    def value(self, content):
        return IDCTimes(content).modified or self.default


class SortByCreation(object):
    interface.implements(ISortingType)

    title = _(u'Sort by creation time')
    description = u''
    default = datetime(2000, 1, 1, tzinfo=utc)

    def value(self, content):
        return IDCTimes(content).created or self.default
