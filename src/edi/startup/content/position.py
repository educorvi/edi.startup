# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer

from edi.startup import _

class IPosition(model.Schema):
    """ Marker interface and Dexterity Python Schema for Position
    """
    start = schema.Datetime(title=_("Start of performance period"), required=True)
    end = schema.Datetime(title=_("End of performance period"), required=True)

    hours_practice = schema.Int(title=_("Hours of temporary staff or pupils"), required=True, default=0)
    hours_trainee = schema.Int(title=_("Hours of trainees or students"), required=True, default=0)
    hours_professional = schema.Int(title=_("Hours of professionals"), required=True, default=0)
    hours_expert = schema.Int(title=_("Hours of experts"), required=True, default=0)


@implementer(IPosition)
class Position(Item):
    """ Content-type class for IPosition
    """
