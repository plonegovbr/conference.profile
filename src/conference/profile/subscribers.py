# -*- coding: utf-8 -*-
from five import grok

from plone.namedfile import NamedImage

from zope.app.container.interfaces import IObjectAddedEvent

from Products.CMFCore.utils import getToolByName

from collective.person.behaviors.user import IPloneUser

from conference.profile.content.profile import IPersonProfile


@grok.subscribe(IPersonProfile, IObjectAddedEvent)
def profile_added(context, event):
    # Set user_name to the owner of the profile
    owner = context.getOwner()
    plone_user = IPloneUser(context)
    if owner and not plone_user.user_name:
        mt = getToolByName(context, 'portal_membership')
        plone_user.user_name = owner.getId()
        # Set values from user registration
        context.location = owner.getProperty('location')
        context.gender = owner.getProperty('gender')
        context.email = owner.getProperty('email')
        context.twitter = owner.getProperty('twitter')
        portrait = mt.getPersonalPortrait(owner.getId())
        # Set portrait, if exists
        if not portrait.getId() == 'defaultUser.png':
            # image/png image/jpeg
            ext = portrait.content_type.split('/')[1]
            raw_data = portrait.data
            image = NamedImage(raw_data,
                               filename=u'%s.%s' % (portrait.getId(), ext))
            context.picture = image
