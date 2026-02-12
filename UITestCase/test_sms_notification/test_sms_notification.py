# Author:Yi Sun(Tim) 2024-05-21

'''Test SMS Notification Page'''

import pytest
from UIModule.sms_notification import *

class Test_SMS_Notification( ):

    def test_sms_ui_001(self,sms_notification):
        '''Verify the URL'''
        assert sms_notification.check_sms_url == 'https://test'

    def test_sms_ui_002(self,sms_notification):
        '''Verify the Title'''
        assert sms_notification.check_sms_title == 'SMS Notification'

    def test_sms_ui_003(self,sms_notification):
        '''Verify the default values'''
        expected =('ECO_API_KEY','Eco2023!','+6100000000')
        actual = sms_notification.check_default_value
        assert actual == expected,f"Expected:{expected},but got: {actual}"

    def test_sms_ui_004(self,sms_notification):
        '''Verify the apikey box status'''
        assert sms_notification.check_apikey_disable is False

    def test_sms_ui_005(self,sms_notification):
        '''Verify the password box status'''
        assert sms_notification.check_pwd_disable is False

    def test_sms_ui_006(self,sms_notification):
        '''Verify the From box status'''
        assert sms_notification.check_from_disable is False

    def test_sms_ui_007(self,sms_notification):
        '''Verify the tab screen'''
        expected = ('MLB-Install','SYD-Install')
        actual = sms_notification.check_tab
        assert actual == expected,f"Expected:{expected},but got: {actual}"

    def test_sms_ui_008(self,sms_notification):
        '''Verify the Production Enter in MLB-Install tab screen'''
        expected = 'MLB Install - In Production Entered'
        actual = sms_notification.check_mlb_enter
        assert expected in actual,f"Expected '{expected}' to be in '{actual}'"

    def test_sms_ui_009(self,sms_notification):
        '''Verify the Production Rollforming in MLB-Install tab screen'''
        expected = 'MLB Install - In Production Roll Forming'
        actual = sms_notification.check_mlb_rollforming
        assert expected in actual, f"Expected '{expected}' to be in '{actual}'"

    def test_sms_ui_010(self,sms_notification):
        '''Verify the Production QC Pass in MLB-Install tab screen'''
        expected = 'MLB Install - In Production QC Pass'
        actual = sms_notification.check_mlb_qcpass
        assert expected in actual, f"Expected '{expected}' to be in '{actual}'"