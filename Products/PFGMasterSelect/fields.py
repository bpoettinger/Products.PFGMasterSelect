from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.Archetypes.Field import StringField
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField import SelectColumn
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.PloneFormGen.content.fieldsBase import BaseFormField, BaseFieldSchemaStringDefault, vocabularyField, \
    vocabularyOverrideField, LinesVocabularyField, StringVocabularyField
from zope.interface import implements
from .interfaces import IFormMasterSelectStringField, IFormMasterMultiSelectStringField
from Products.PFGMasterSelect.config import PROJECTNAME


FormMasterSelectFieldSchema = BaseFieldSchemaStringDefault.copy() + atapi.Schema((
    vocabularyField,
    vocabularyOverrideField,
    DataGridField('slave_fields',
                  allow_insert=True,
                  allow_delete=True,
                  allow_reorder=True,
                  columns=('name', 'action', 'vocab_method', 'toggle_method', 'hide_values'),
                  widget=DataGridWidget(label='Slave Fields',
                                        description='Configure actions applied on other fields of the Form Folder '
                                                    'when changing this fields state. The new value of this field '
                                                    'is available as "value" in vocab_method and toggle_method.',
                                        columns={
                                              'name': SelectColumn('Name', 'getNameVocab'),
                                              'action': SelectColumn('Action', 'getActionVocab'),
                                        }),
                  ),
))

schemata.finalizeATCTSchema(FormMasterSelectFieldSchema, moveDiscussion=False)


class FormMasterSelectStringField(BaseFormField):

    implements(IFormMasterSelectStringField)

    meta_type = "FormMasterSelectStringField"
    schema = FormMasterSelectFieldSchema

    def __init__(self, oid, **kwargs):
        BaseFormField.__init__(self, oid, **kwargs)

        self.fgField = StringVocabularyField('fg_masterselect',
                                             searchable=False,
                                             required=False,
                                             vocabulary=None,
                                             widget=MasterSelectWidget(slave_fields=[]))

    def setSlave_fields(self, slave_fields):
        self.Schema()['slave_fields'].set(self, slave_fields)
        self.fgField.widget.slave_fields = slave_fields

    def getActionVocab(self):
        return atapi.DisplayList((
            ('hide', 'Hide'),
            ('show', 'Show'),
            ('enable', 'Enable'),
            ('disable', 'Disable'),
            ('value', 'Value'),
            ('vocabulary', 'Vocabulary'),
        ))

    def getNameVocab(self):
        folder = self.aq_parent
        fieldNames = [field.getName() for field in folder.fgFields()]
        return atapi.DisplayList(zip(fieldNames, fieldNames))


FormMasterMultiSelectFieldSchema = BaseFieldSchemaStringDefault.copy() + atapi.Schema((
    vocabularyField,
    vocabularyOverrideField,
    DataGridField('slave_fields',
                  allow_insert=True,
                  allow_delete=True,
                  allow_reorder=True,
                  columns=('name', 'action', 'vocab_method', 'toggle_method', 'hide_values'),
                  widget=DataGridWidget(label='Slave Fields',
                                        description='Configure actions applied on other fields of the Form Folder '
                                                    'when changing this fields state. The currently selected values of '
                                                    'this field is available as "values" in vocab_method and '
                                                    'toggle_method.',
                                        columns={
                                         'name': SelectColumn('Name', 'getNameVocab'),
                                         'action': SelectColumn('Action', 'getActionVocab'),
                                        }),
                  ),
))

schemata.finalizeATCTSchema(FormMasterMultiSelectFieldSchema, moveDiscussion=False)


class FormMasterMultiSelectStringField(BaseFormField):

    implements(IFormMasterMultiSelectStringField)

    meta_type = "FormMasterMultiSelectStringField"
    schema = FormMasterMultiSelectFieldSchema

    def __init__(self, oid, **kwargs):
        BaseFormField.__init__(self, oid, **kwargs)

        self.fgField = LinesVocabularyField('fg_masterselect',
                                            searchable=False,
                                            required=False,
                                            vocabulary=None,
                                            multiValued=True,
                                            widget=MasterMultiSelectWidget(slave_fields=[]))

    def setSlave_fields(self, slave_fields):
        self.Schema()['slave_fields'].set(self, slave_fields)
        self.fgField.widget.slave_fields = slave_fields

    def getActionVocab(self):
        return atapi.DisplayList((
            ('hide', 'Hide'),
            ('show', 'Show'),
            ('enable', 'Enable'),
            ('disable', 'Disable'),
            ('value', 'Value'),
            ('vocabulary', 'Vocabulary'),
        ))

    def getNameVocab(self):
        folder = self.aq_parent
        fieldNames = [field.getName() for field in folder.fgFields()]
        return atapi.DisplayList(zip(fieldNames, fieldNames))


atapi.registerType(FormMasterSelectStringField, PROJECTNAME)
atapi.registerType(FormMasterMultiSelectStringField, PROJECTNAME)