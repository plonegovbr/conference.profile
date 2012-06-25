# -*- coding:utf-8 -*-
import hashlib
import urllib

from Acquisition import aq_inner

from five import grok
from conference.profile.content.profile import IPersonProfile


class View(grok.View):
    grok.context(IPersonProfile)
    grok.require('zope2.View')


class PictureView(grok.View):
    grok.context(IPersonProfile)
    grok.require('zope2.View')
    grok.name('picture')

    template = None

    default = "http://www.example.com/default.jpg"

    def gravatar(self, size=150):
        ''' Return gravatar url for this profile '''
        email = aq_inner(self.context).email
        gravatar_url = ("http://www.gravatar.com/avatar/" +
                        hashlib.md5(email.lower()).hexdigest() +
                        "?")
        gravatar_url += urllib.urlencode({'d': self.default, 's': str(size)})
        return gravatar_url

    def picture(self, size=150):
        ''' Return profile picture '''
        context = aq_inner(self.context)
        picture = context.picture
        if picture:
            scale = context.unrestrictedTraverse('@@images')
            picture_scale = scale.scale('picture',
                                        width=size,
                                        height=size)
            return picture_scale

    def picture_tag(self, size=150):
        ''' Return a tag for this picture '''
        picture = self.picture(size)
        if picture:
            return picture.tag()
        else:
            context = aq_inner(self.context)
            title = context.title
            w = h = size
            url = self.gravatar(size)
            return ('''<img src='%s' title='%s' width='%d' height='%d'>''' %
                    (url, title, w, h))

    def render(self):
        ''' '''
        return self.picture_tag(size=150)
