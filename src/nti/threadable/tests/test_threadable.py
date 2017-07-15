#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import unittest

from nti.threadable.interfaces import IThreadable

from nti.threadable.threadable import Threadable

from nti.threadable.tests import SharedConfiguringTestLayer


class TestThreadable(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_interface(self):
        threadable = Threadable()
        assert_that(threadable, validly_provides(IThreadable))
        assert_that(threadable, verifiably_provides(IThreadable))
