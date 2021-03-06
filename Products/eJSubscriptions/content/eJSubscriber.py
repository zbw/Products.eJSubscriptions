# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.eJSubscriptions.interfaces import IeJSubscriber
from Products.eJSubscriptions.config import *

from Products.CMFCore.utils import getToolByName
#from zope.component import getUtility
#from Products.eJournal.interfaces.utilities import IEjournalSettings
from Products.eJournal import settings



schema = Schema((
    
#   BooleanField(
#     name="all_jels",
#     regfield="1",
#     default=True,
#     widget=BooleanWidget(
#       label="On all JEL classes",
#       description="Check this to get notifications on all new papers",
#     )
#   ),

    LinesField(
        name='jel',
        widget=InAndOutWidget
        (
            label=' E-mail alert only on new papers with the following JEL classifications',
            description="Select the JELs inside the left box \
                and then click the arrow to get them into the right box,\
                which is the actual list.\n",
            label_msgid='eJSubscriptions_label_jel',
            i18n_domain='eJournal',
        ),
        enforceVocabulary=1,
        vocabulary="_getJEL"
    ),

    

),


)


eJSubscriber_schema = BaseSchema.copy() + \
    schema.copy()

eJSubscriber_schema["title"].widget.label = "E-Mail"
eJSubscriber_schema["title"].write_permission = "Manage portal"

class eJSubscriber(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)
    
    implements(IeJSubscriber)

    # This name appears in the 'add' box
    archetype_name = 'eJSubscriber'

    _at_rename_after_creation = True

    schema = eJSubscriber_schema

    def setEmail(self, value):
        """
        """
        self.getField("title").set(self, value)

    def getEmail(self):
        """
        """
        return self.getField("title").get(self)

    def _getJEL(self):
        """
        """
        return settings.jels


    def setJel(self, value):
        """Overwritten to sort JEL classes.
        """
        value = list(value)
        value.sort()
        self.getField('jel').set(self, value)

registerType(eJSubscriber, PROJECTNAME)

