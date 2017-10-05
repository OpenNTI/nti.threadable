#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_entry
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property

import fudge
import unittest

from nti.threadable.tests import PThreadable
from nti.threadable.tests import PInternalObjectIO
from nti.threadable.tests import SharedConfiguringTestLayer


class TestExternalization(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @fudge.patch('nti.threadable.externalization.to_external_ntiid_oid')
    def test_export(self, mock_oid):
        inReplyTo = PThreadable()
        context = PThreadable()
        context.inReplyTo = inReplyTo
        pio = PInternalObjectIO(context)
        # no oid
        mock_oid.is_callable().returns(None)
        with self.assertRaises(ValueError):
            pio.toExternalObject()
        mock_oid.calls(lambda x: str(id(x)))
        assert_that(pio.toExternalObject(),
                    has_entry('inReplyTo', is_not(none())))

        # don't write missing references
        context = PThreadable()

        class NoneRef(object):
            def __conform__(self, unused):
                return None

            def __call__(self):
                return None
        pio = PInternalObjectIO(context)
        pio._ext_write_missing_references = False

        context._inReplyTo = NoneRef()
        assert_that(pio.toExternalObject(),
                    has_entry('inReplyTo', is_(none())))

        # write missing references
        pio._ext_write_missing_references = True
        assert_that(pio.toExternalObject(),
                    has_entry('inReplyTo', is_(none())))

        # write missing ntiid
        class MissingNTIIDRef(object):
            def __conform__(self, unused):
                return self

            def __call__(self):
                return None

            def make_missing_ntiid(self):
                return "missing"

        context._inReplyTo = MissingNTIIDRef()
        assert_that(pio.toExternalObject(),
                    has_entry('inReplyTo', 'missing'))

    def test_import(self):
        context = PThreadable()
        assert_that(context, has_property('inReplyTo', is_(none())))
        assert_that(context, has_property('references', is_(())))

        pio = PInternalObjectIO(context)
        pio.updateFromExternalObject({'inReplyTo':  PThreadable(),
                                      'references': [PThreadable()]})
        assert_that(context, has_property('inReplyTo', is_not(none())))
        assert_that(context, has_property('references', has_length(1)))
