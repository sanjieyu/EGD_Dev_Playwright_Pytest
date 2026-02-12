# Author:Yi Sun(Tim) 2024-05-21

import pytest
from UIModule.sms_notification import SMS_Notification


@pytest.fixture(scope="class")
def sms_notification(page_in_class,credentials):
    page_in_class.goto(credentials["egd_url"])
    page_in_class.wait_for_load_state("networkidle")
    sms_notification_page = SMS_Notification(page_in_class)
    try:
        sms_notification_page.go_sms_notification()
    except Exception as e:
        print(f"fail to goto the correct URL: {page_in_class.url}")
        raise e
    return sms_notification_page

