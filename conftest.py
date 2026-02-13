# Author:Yi Sun(Tim) 2024-1-22

import pytest
import os
from utils.read_config import ReadConfig

@pytest.fixture(scope="session")
def config_reader():
    return ReadConfig()
@pytest.fixture(scope="session")
def credentials(config_reader):
    return {
        "egd_url": config_reader.get_url(),
        "admin_username": config_reader.admin_username(),
        "admin_password": config_reader.admin_password(),
        "dealer_username": config_reader.dealer_username(),
        "dealer_password": config_reader.dealer_password()
    }

@pytest.fixture(scope="session")
def base_url(credentials):
    return credentials["egd_url"]

# def pytest_sessionfinish(session, exitstatus):
#     try:
#         from CommonModule.send_report import ReportSender
#         sender = ReportSender()
#         sender.send_email(report_path="Report/report.html")
#     except ModuleNotFoundError:
#         print("\n[Error] Can't send report：CommonModule.send_report module missing")
#     except Exception as e:
#         print(f"\n[Error] Failed to send report: {e}")


