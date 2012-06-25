# -*- coding:utf-8 -*-
from zope import schema
from zope.interface import implements

from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider

from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

from collective.person.content.person import gender_options

from conference.profile import MessageFactory as _


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IConferenceUserDataSchema


class IConferenceUserDataSchema(IUserDataSchema):
    ''' Add a gender field to the registration form '''

    gender = schema.Choice(
        title=_(u"Gender"),
        description=_(u""),
        required=False,
        source=gender_options,
        )

    twitter = schema.TextLine(
        title=_(u"Twitter"),
        description=_(u"Please inform your twitter account."),
        required=False,
        )


class ConferenceUserDataPanelAdapter(UserDataPanelAdapter):
    """ Override default plone adapter
    """
    @property
    def gender(self):
        return self.context.getProperty('gender', '')

    @gender.setter
    def gender(self, value):
        return self.context.setMemberProperties({'gender': value})

    @property
    def twitter(self):
        return self.context.getProperty('twitter', '')

    @twitter.setter
    def twitter(self, value):
        return self.context.setMemberProperties({'twitter': value})
