#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property

import unittest

import BTrees

from zope import component
from zope import interface

from zope.intid.interfaces import IIntIds

from persistent import Persistent

from nti.threadable.interfaces import IThreadable

from nti.threadable.subscribers import discard

from nti.threadable.subscribers import threadable_added
from nti.threadable.subscribers import _do_threadable_added

from nti.threadable.subscribers import threadable_removed

from nti.threadable.tests import PThreadable
from nti.threadable.tests import SharedConfiguringTestLayer


class TestSubscribers(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_discard(self):
        # coverage
        discard([1], 1)
        discard([1], 2)

    def test_threadable_added(self):

        class MockIntIds(object):
            family = BTrees.family64

            def getId(self, obj):
                return id(obj)

        intids = MockIntIds()
        component.getGlobalSiteManager().registerUtility(intids, IIntIds)

        context = PThreadable()
        # no ops
        threadable_added(context, None)
        threadable_removed(context, None)

        # no ops no threadable reply
        context.inReplyTo = Persistent()
        _do_threadable_added(context, intids, id(context))
        threadable_removed(context, None)

        # added
        inReplyTo = PThreadable()
        context.inReplyTo = inReplyTo
        threadable_added(context, None)

        assert_that(inReplyTo,
                    has_property('_replies', has_length(1)))

        assert_that(inReplyTo,
                    has_property('_referents', has_length(1)))

        # removed
        # from IPython.terminal.debugger import set_trace;set_trace()
        threadable_removed(context, None)

        # coverage
        @interface.implementer(IThreadable)
        class FakeThreadable(Persistent):
            inReplyTo = None
        inReplyTo = FakeThreadable()
        context.inReplyTo = inReplyTo
        threadable_removed(context, None)
        component.getGlobalSiteManager().unregisterUtility(intids, IIntIds)
