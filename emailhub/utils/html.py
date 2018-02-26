# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def icon(name, tooltip=None, css_class=None):
    _ctx = {'icon': name}
    _class = ['material-icons']
    if tooltip:
        _class.append('tooltip')
        _ctx['tooltip'] = ' data-tooltip="%s"' % tooltip
    else:
        _ctx['tooltip'] = ' '
    if css_class:
        _class.append(css_class)
    _ctx['class'] = ' '.join(_class)
    return '<i class="%(class)s"%(tooltip)s>%(icon)s</i>' % _ctx
