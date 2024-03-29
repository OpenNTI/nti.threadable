#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ
# pylint: disable=inherit-non-class

import unittest

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin

import zope.testing.cleanup


class SharedConfiguringTestLayer(GCLayerMixin,
                                 ZopeComponentLayer,
                                 ConfiguringLayerMixin):

    set_up_packages = ('nti.threadable',)

    @classmethod
    def setUp(cls):
        cls.setUpPackages()

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        zope.testing.cleanup.cleanUp()

    @classmethod
    def testSetUp(cls, test=None):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class ThreadableLayerTest(unittest.TestCase):
    layer = SharedConfiguringTestLayer


from zope import interface

from persistent import Persistent

from nti.externalization.datastructures import InterfaceObjectIO

from nti.threadable.threadable import Threadable

from nti.threadable.externalization import ThreadableExternalizableMixin


class IPThreadable(interface.Interface):
    pass


@interface.implementer(IPThreadable)
class PThreadable(Persistent, Threadable):
    pass


class PInternalObjectIO(ThreadableExternalizableMixin,
                        InterfaceObjectIO):
    _ext_iface_upper_bound = IPThreadable
