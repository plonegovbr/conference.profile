# -*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from conference.profile.testing import FUNCTIONAL_TESTING

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_ONLY_FIRST_FAILURE)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('user_registration.txt',
                                     optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
