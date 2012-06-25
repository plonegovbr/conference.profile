# -*- coding: utf-8 -*-
import unittest2 as unittest

from AccessControl import Unauthorized

from zope.component import createObject
from zope.component import queryUtility

from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.uuid.interfaces import IAttributeUUID

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import logout
from plone.app.testing import login

from plone.dexterity.interfaces import IDexterityFTI

from collective.person.behaviors.user import IPloneUser

from conference.profile.content.profile import IPersonProfile

from conference.profile.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.members = self.portal['Members']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_adding_as_manager_at_site_root(self):
        # Only allows Members folder
        self.assertRaises(Unauthorized,
                          self.portal.invokeFactory,
                          *('conference.profile', 'guido'))

    def test_adding_as_manager_at_members_folder(self):
        self.members.invokeFactory('conference.profile', 'guido')
        profile = self.members['guido']
        self.assertTrue(IPersonProfile.providedBy(profile))

    def test_adding_as_editor_at_members_folder(self):
        setRoles(self.portal, TEST_USER_ID, ['Editor'])
        self.members.invokeFactory('conference.profile', 'guido')
        profile = self.members['guido']
        self.assertTrue(IPersonProfile.providedBy(profile))

    def test_adding_member_unauthorized(self):
        # Set user roles as Member
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.assertRaises(Unauthorized,
                          self.members.invokeFactory,
                          *('conference.profile', 'guido'))

    def test_adding_anonymous_unauthorized(self):
        logout()
        self.assertRaises(Unauthorized,
                          self.members.invokeFactory,
                          *('conference.profile', 'guido'))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='conference.profile')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='conference.profile')
        schema = fti.lookupSchema()
        self.assertEquals(IPersonProfile, schema)

    def test_is_referenceable(self):
        self.members.invokeFactory('conference.profile', 'guido')
        profile = self.members['guido']
        self.assertTrue(IReferenceable.providedBy(profile))
        self.assertTrue(IAttributeUUID.providedBy(profile))

    def test_plone_user_behavior(self):
        self.members.invokeFactory('conference.profile', 'guido')
        profile = self.members['guido']
        plone_user = IPloneUser(profile)
        self.assertNotEquals(None, plone_user)
        self.assertEquals(plone_user.user_name, TEST_USER_ID)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='conference.profile')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IPersonProfile.providedBy(new_object))


class MemberAreaTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.membership = self.portal.portal_membership
        self.wt = self.portal.portal_workflow
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_creation(self):
        self.assertEqual(self.membership.getHomeFolder(), None)
        self.portal.logged_in()
        self.failIfEqual(self.membership.getHomeFolder(), None)
        home = self.membership.getHomeFolder()
        self.assertEqual(home.portal_type, 'conference.profile')

    def test_areatitle(self):
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        self.assertEqual(home.given_name, 'test_user_1_')
        self.assertEqual(home.surname, '')
        self.assertEqual(home.fullname, 'test_user_1_ ')

    def test_area_attributes(self):
        member = self.membership.getAuthenticatedMember()
        member.setMemberProperties(
                    {'email': 'products@simplesconsultoria.com.br',
                     'gender': 'm',
                     'twitter': '@simplesconsult',
                     'fullname': 'Simples Consultoria'})
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        self.assertEqual(home.given_name, 'Simples')
        self.assertEqual(home.surname, 'Consultoria')
        self.assertEqual(home.fullname, 'Simples Consultoria')
        self.assertEqual(home.gender, 'm')
        self.assertEqual(home.twitter, '@simplesconsult')

    def test_ownership(self):
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        user = self.membership.getAuthenticatedMember()
        roles = user.getRolesInContext(home)
        self.assertTrue('Owner' in roles)

    def test_workflow_state(self):
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        review_state = self.wt.getInfoFor(home, 'review_state')
        self.assertEquals(review_state, 'published')

    def test_exclude_from_nav(self):
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        exclude_from_nav = home.exclude_from_nav
        self.assertEquals(exclude_from_nav, True)

    def test_user_name(self):
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        plone_user = IPloneUser(home)
        self.assertEquals(plone_user.user_name, TEST_USER_ID)

    def test_picture_gravatar(self):
        member = self.membership.getAuthenticatedMember()
        member.setMemberProperties(
                    {'email': 'products@simplesconsultoria.com.br',
                     'gender': 'm',
                     'twitter': '@simplesconsult',
                     'fullname': 'Simples Consultoria'})
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        picture_tag = home.restrictedTraverse('@@picture')()
        self.assertTrue('http://www.gravatar.com/avatar/' in picture_tag)
        self.assertTrue('99300d2354bc942e6bccc771d0ad443d' in picture_tag)
        self.assertTrue("title='Simples Consultoria' width='150' height='150'>"
                        in picture_tag)

    def test_picture_uploaded(self):
        import os
        from Products.PlonePAS.tests import dummy
        from conference.profile import tests
        member = self.membership.getAuthenticatedMember()
        member.setMemberProperties(
                    {'email': 'products@simplesconsultoria.com.br',
                     'gender': 'm',
                     'twitter': '@simplesconsult',
                     'fullname': 'Simples Consultoria'})
        image = open(os.path.join(os.path.dirname(tests.__file__),
                             'user_portrait.png'))
        image_upload = dummy.FileUpload(dummy.FieldStorage(image))
        self.membership.changeMemberPortrait(image_upload,
                                            member.getMemberId())
        self.portal.logged_in()
        home = self.membership.getHomeFolder()
        picture_tag = home.restrictedTraverse('@@picture')()
        self.assertTrue('http://nohost/plone/' in picture_tag)
        self.assertTrue('Members/test_user_1_/@@images/' in picture_tag)
        self.assertTrue('title="Simples Consultoria"' in picture_tag)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
