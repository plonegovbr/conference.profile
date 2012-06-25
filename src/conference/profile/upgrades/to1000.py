# -*- coding: utf-8 -*-
from collective.grok import gs

from Products.CMFCore.utils import getToolByName


def use_memberarea(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    mt = getToolByName(portal, 'portal_membership')
    mt.memberarea_type = 'conference.profile'
    mt.membersfolder_id = 'Members'
    mt.memberareaCreationFlag = True
    # Create base folder
    if not 'Members' in portal.objectIds():
        portal.invokeFactory(type_name='Folder',
                             id='Members',
                             title='Conference Members')
    # Set permission just on Members folder
    members = portal['Members']
    members.manage_permission('conference.profile: Add Profile',
                              roles=('Manager', 'Editor'), acquire=0)


@gs.upgradestep(title=u'Initial upgrade steo',
                description=u'Upgrade step run at install time',
                source='*', destination='1000', sortkey=1,
                profile='conference.profile:default')
def fromZero(context):
    """ Upgrade from Zero to version 1000
    """
    use_memberarea(context)
