# -*- coding:utf-8 -*-
from five import grok

from zope import schema

from plone.directives import form

from collective.person.content.person import IPerson
from collective.person.content.person import Person

from conference.profile import MessageFactory as _


class IPersonProfile(IPerson):
    """
    A profile for a user in the conference
    """
    form.omitted('birthday')

    email = schema.TextLine(
        title=_(u"E-mail"),
        description=_(u"Please inform your email."),
        required=True,
        )

    twitter = schema.TextLine(
        title=_(u"Twitter"),
        description=_(u"Please inform your twitter account."),
        required=False,
        )

    location = schema.TextLine(
        title=_(u"Location"),
        description=_(u"Where are you from?"),
        required=False,
        )


class PersonProfile(Person):
    grok.implements(IPersonProfile)
    # Add your class methods and properties here

    exclude_from_nav = True

    def setTitle(self, value):
        ''' Membership tool expects a setTitle '''
        title = value.split(' ')
        given_name = surname = ''
        if len(title) == 2:
            given_name = title[0]
            surname = title[1]
        elif len(title) == 1:
            given_name = title[0]
            surname = ''
        elif len(title) > 2:
            given_name = title[0]
            surname = ' '.join(title[1:])
        else:
            # Overide here
            given_name = ''
            surname = ''
        self.given_name = given_name
        self.surname = surname
