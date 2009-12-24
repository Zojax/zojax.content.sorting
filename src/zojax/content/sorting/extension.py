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
from BTrees.IFBTree import IFBTree
from BTrees.OOBTree import OOBTree, OOSet

from zope import interface, component
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zope.app.intid.interfaces import IIntIdAddedEvent
from zope.app.intid.interfaces import IIntIdRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IContent

from interfaces import ISorting, ISortable, ISortingType


class SortingExtension(object):
    interface.implements(ISorting)

    @property
    def index(self):
        index = self.data.get('index')
        if index is None:
            index = IFBTree()
            self.data['index'] = index
            self.rebuild()

        return index

    @property
    def mapping(self):
        mapping = self.data.get('mapping')
        if mapping is None:
            mapping = OOBTree()
            self.data['mapping'] = mapping

        return mapping

    def addItem(self, name):
        item = self.context[name]
        id = getUtility(IIntIds).queryId(removeAllProxies(item))
        if id is None:
            return

        value = getUtility(ISortingType, name=self.type).value(item)

        self.mapping[id] = value

        index = self.index
        index.clear()

        data = OOSet([(v, k) for k, v in self.mapping.items()])

        idx = 1.0
        for v, id in data:
            index[id] = idx
            idx += 1.0

    def updateItem(self, name):
        if name not in self.context:
            return

        item = self.context[name]
        id = getUtility(IIntIds).getId(removeAllProxies(item))
        value = getUtility(ISortingType, name=self.type).value(item)

        if (id in self.mapping) and (self.mapping[id] == value):
            return
        else:
            self.addItem(name)

    def removeItem(self, name):
        item = self.context[name]
        id = getUtility(IIntIds).queryId(removeAllProxies(item))
        if id is not None and id in self.index:
            del self.index[id]
            del self.mapping[id]

    def getItems(self):
        ids = getUtility(IIntIds)

        contextId = ids.queryId(removeAllProxies(self.context))
        if contextId:
            items = getUtility(ICatalog).searchResults(
                sort_order=(self.order=='direct' and 'reverse' or ''),
                sortingContext={'any_of': (contextId,)},
                noPublishing=True)
            items.applySorting(self.index)
            return items
        else:
            return ()

    def rebuild(self):
        self.index.clear()
        self.mapping.clear()

        context = self.context
        for name in context.keys():
            self.addItem(name)


@component.adapter(ISorting, IObjectModifiedEvent)
def sortingExtensionModified(ext, event):
    ext.rebuild()


@component.adapter(IContent, IObjectModifiedEvent)
def contentModified(content, event):
    content = removeAllProxies(content)
    if ISortable.providedBy(content.__parent__):
        ISorting(content.__parent__).updateItem(content.__name__)


@component.adapter(IIntIdAddedEvent)
def idAdded(event):
    object = event.object
    parent = getattr(object, '__parent__', None)
    if ISortable.providedBy(parent):
        ISorting(removeAllProxies(parent)).updateItem(object.__name__)


@component.adapter(IIntIdRemovedEvent)
def idRemoved(event):
    object = event.object
    parent = getattr(object, '__parent__', None)
    if ISortable.providedBy(parent):
        ISorting(removeAllProxies(parent)).removeItem(object.__name__)
