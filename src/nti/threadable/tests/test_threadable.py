#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import unittest

from zope import component

from zope.intid.interfaces import IIntIds

from nti.threadable.interfaces import IThreadable

from nti.threadable.threadable import Threadable

from nti.threadable.tests import SharedConfiguringTestLayer


class TestThreadable(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_model(self):
        threadable = Threadable()
        assert_that(threadable, validly_provides(IThreadable))
        assert_that(threadable, verifiably_provides(IThreadable))
        
        assert_that(threadable.isOrWasChildInThread(),
                    is_(False))
        
        assert_that(threadable,
                    has_property('replies', is_(())))
        
        assert_that(threadable,
                    has_property('referents', is_(())))
        
        assert_that(threadable,
                    has_property('most_recent_reply', is_(none())))

        
        mock = Threadable()
        class MockIntIds(object):
            def getObject(self, unused_doc_id):
                return mock
            
        intids = MockIntIds()
        component.getGlobalSiteManager().registerUtility(intids, IIntIds)
        threadable._replies = [1]
        
        assert_that(list(threadable.replies),
                    is_([mock]))
        
        assert_that(threadable,
                    has_property('most_recent_reply', is_(mock)))
         
        threadable._referents = [1]
        assert_that(list(threadable.referents),
                    is_([mock]))
        
        component.getGlobalSiteManager().unregisterUtility(intids, IIntIds)
