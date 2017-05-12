import json

import logging

import Products
from App.Common import aq_base
from Products.Archetypes import DisplayList
from Products.Five import BrowserView
from Products.MasterSelectWidget.browser import JSONValuesForAction, SetupSlaves
from Products.PloneFormGen.content.form import FormFolder
from zope.i18n import translate


class Migration(BrowserView):

    def fix_write_permissions(self):
        catalog = self.context.portal_catalog

        logger = logging.getLogger('PFGMasterSelect')

        for brain in catalog(portal_type=('FormMasterSelectStringField', 'FormMasterMultiSelectStringField',)):
            obj = brain.getObject()

            from Products.CMFCore.permissions import View
            obj.fgField.write_permission = View

            logger.warning('Fixed write permission of object %s' % '/'.join(obj.getPhysicalPath()))


class SetupSlaves(SetupSlaves):
    pass


class JSONValuesForAction(JSONValuesForAction):

    def evaluate_method(self, method, args):
        # Assumptions:
        # There are two possibilities: This is called on a (a) single select field or (b) multi select field.
        # In case (a) there should always be exactly one value, hence len(args) == 1, and it should not be a
        # dictionary. On the other hand in case (b) there can be an arbitrary count of elements selected and all
        # elements are stored in dictionaries.
        if len(args) == 0 or isinstance(args[0], dict):
            l = dict(values=[arg['val'] for arg in args if arg['selected']])
        else:
            assert len(args) == 1
            l = dict(value=args[0])
        g = dict(__builtins__=globals()['__builtins__'])
        return eval(method, g, l) if method else None

    def getSlaves(self, fieldname):
        assert isinstance(self.context, FormFolder)

        field_object = self.context.findFieldObjectByName(fieldname)
        slave_fields = field_object.fgField.widget.slave_fields or ()
        return slave_fields

    def __call__(self):
        assert isinstance(aq_base(self.context), FormFolder)
        return Products.MasterSelectWidget.browser.JSONValuesForAction.__call__(self)


class JSONValuesForVocabularyChange(JSONValuesForAction):

    def computeJSONValues(self, slave, args):
        vocabulary = self.evaluate_method(slave['vocab_method'], args)
        vocabulary = [str(item) for item in vocabulary]
        vocabulary = DisplayList(zip(vocabulary, vocabulary))

        return json.dumps([
                dict(
                    value=item,
                    label=translate(vocabulary.getValue(item), context=self.request)
                ) for item in vocabulary
            ])


class JSONValuesForValueUpdate(JSONValuesForAction):

    def computeJSONValues(self, slave, args):
        value = self.evaluate_method(slave['vocab_method'], args)
        return json.dumps(translate(value, context=self.request))


class JSONValuesForToggle(JSONValuesForAction):

    def computeJSONValues(self, slave, args):
        expression = slave['toggle_method']
        if expression:
            toggle = self.evaluate_method(slave['toggle_method'], args)
        else:
            hide_values = slave.get('hide_values')
            hide_values = eval(hide_values, None, None) if hide_values else ()

            if not isinstance(hide_values, (list, tuple)):
                hide_values = (hide_values,)
            values = []
            for val in hide_values:
                if not isinstance(val, str):
                    val = str(val)
                values.append(val)
            toggle = str(args[0]) in values

        action = self.action
        if action in ['disable', 'hide']:
            toggle = not toggle
            action = action == 'disable' and 'enable' or 'show'
        json_toggle = json.dumps({'toggle': toggle, 'action': action})

        return json_toggle
