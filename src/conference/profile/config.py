# -*- coding:utf-8 -*-
from five import grok

from collective.grok import gs
from collective.grok import i18n

from Products.CMFPlone.interfaces import INonInstallable

from conference.profile import MessageFactory as _

PROJECTNAME = 'conference.profile'
PROFILE_ID = 'conference.profile:default'


# Default Profile
gs.profile(name=u'default',
           title=_(u'conference.profile'),
           description=_(u'Installs conference.profile'),
           directory='profiles/default')

# Uninstall Profile
gs.profile(name=u'uninstall',
           title=_(u'Uninstall conference.profile'),
           description=_(u'Uninstall conference.profile'),
           directory='profiles/uninstall')

i18n.registerTranslations(directory='locales')


class HiddenProfiles(grok.GlobalUtility):

    grok.implements(INonInstallable)
    grok.provides(INonInstallable)
    grok.name('conference.profile')

    def getNonInstallableProfiles(self):
        profiles = ['conference.profile:uninstall', ]
        return profiles
