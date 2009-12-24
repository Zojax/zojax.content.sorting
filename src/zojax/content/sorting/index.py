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
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zc.catalog.catalogindex import ValueIndex
from zojax.catalog.utils import Indexable
from zojax.content.sorting.interfaces import ISortable


def sortingContextIndex():
    return ValueIndex(
        'value', Indexable('zojax.content.sorting.index.SortingContext'))


class SortingContext(object):

    def __init__(self, content, default=None):
        parent = content.__parent__

        if ISortable.providedBy(parent):
            self.value = getUtility(IIntIds).queryId(parent)
        else:
            self.value = default
