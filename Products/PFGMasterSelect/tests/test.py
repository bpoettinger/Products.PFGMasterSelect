import unittest
from plone.testing.z2 import Browser

import transaction
from Products.PFGMasterSelect.testing import MASTER_SELECT_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID, setRoles


class Test(unittest.TestCase):

    layer = MASTER_SELECT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']

        portal = self.portal

        setRoles(self.portal, TEST_USER_ID, ['Manager',])

        portal.invokeFactory('FormFolder', 'formfolder')
        self.form = portal.formfolder

        self.form.invokeFactory('FormMasterSelectStringField', 'master')
        self.master = self.form.master

        self.form.invokeFactory('FormMasterSelectStringField', 'slave')
        slave = self.form.slave

        self.master.setFgVocabulary(['1', '2'])
        self.master.setSlave_fields([dict(name='slave', action='hide', vocab_method='', toggle_method='value in ("1")', hide_values='2')])

        transaction.commit()

        self.browser = Browser(self.app)
        self.browser.handleErrors = False

    def test(self):
        browser = self.browser
        browser.open(self.form.absolute_url() + '/@@masterselect-jsonvalue-toggle?field=master&slave=slave&action=hide&value=1')
        self.assertTrue('"action": "show"' in browser.contents)
        self.assertTrue('"toggle": false' in browser.contents)
