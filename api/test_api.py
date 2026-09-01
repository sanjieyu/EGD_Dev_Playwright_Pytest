# Author:Yi Sun(Tim) 2024-01-15

'''API Testing for Production site'''

import requests
import json
import re
import unittest
from CommonModule.read_excel_title import ExcelData
from CommonModule.read_config import ReadConfig
from bs4 import BeautifulSoup
from parameterized import parameterized


class PRO_API(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.session = requests.Session()
        cls.data = ExcelData().read_excel()

        cls.config_read = ReadConfig()
        cls.base_url = cls.config_read.get_url()
        cls.username = cls.config_read.admin_username()
        cls.password = cls.config_read.admin_password()

        # Fetching Pre-Login Token
        login_page_url = f"{cls.base_url}/Account/Login"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
        print("====== [Step 1] Fetching Pre-Login Token ======")
        response_get = cls.session.get(login_page_url,headers=headers)
        soup = BeautifulSoup(response_get.text,'html.parser')
        token_element = soup.find('input',{'name':'__RequestVerificationToken'})
        if not token_element:
            raise Exception("can't find __RequestVerificationToken from login page")

        anti_forgery_token = token_element.get('value')
        print(f"Get the token successfully: {anti_forgery_token[:20]}...")

        payload = {
            "__RequestVerificationToken": anti_forgery_token,
            "Email": cls.username,
            "Password": cls.password,
            "RememberMe": "false"
        }

        login_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": headers["User-Agent"]
        }

        print("====== [Step 2] Submitting Login Credentials ======")
        response_post = cls.session.post(login_page_url,data=payload,headers=login_headers,allow_redirects=True)

        # Verify Login
        if "Log in" in response_post.text and "Password" in response_post.text:
            raise Exception("Login fail,please check the username or password, or if the token is invalid")
        print("====== [Step 3] Login Success! Session Cookies Saved ======\n")

    def setUp(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()
        print("\n====== All Tests Finished. Session Closed. ======")

    def test_api_01(self):
        """Verify 200 OK status for Get_Quote_Doors"""
        endpoint = self.data[0]['Endpoint']
        self.url = self.base_url + endpoint
        self.r = self.session.request(method=self.data[0]['method'], url=self.url, headers=self.headers)
        self.assertEqual(self.data[0]['return_code'], self.r.status_code)

    def test_api_02(self):
        """Verify Proposal No for Get_Quote_Doors"""
        endpoint = self.data[0]['Endpoint']
        self.url = self.base_url + endpoint
        self.r = self.session.request(method=self.data[1]['method'], url=self.url, headers=self.headers)
        soup = BeautifulSoup(self.r.text, 'html.parser')
        self.proposal_input = soup.find('input', {'id': 'ProposalNo'})
        actual_proposal_no = self.proposal_input.get('value', '').strip()
        print('actual job is: ', actual_proposal_no)
        self.assertEqual(self.data[1]['response'], actual_proposal_no)

    def test_api_03(self):
        """Verify ContactMobile for Get_Quote_Doors"""
        endpoint = self.data[0]['Endpoint']
        self.url = self.base_url + endpoint
        self.r = self.session.request(method=self.data[2]['method'], url=self.url, headers=self.headers)
        soup = BeautifulSoup(self.r.text, 'html.parser')
        self.proposal_input = soup.find('input', {'id': 'ContactMobile'})
        actual_mobile = int(self.proposal_input.get('value', '').strip())
        print('actual ContactMobile is: ', actual_mobile)
        self.assertEqual(self.data[2]['response'], actual_mobile)


    def test_api_04(self):
        """Verify Proposal No for Get_Quote_Doors"""
        endpoint = self.data[6]['Endpoint']
        self.url = self.base_url + endpoint
        self.r = self.session.request(method=self.data[7]['method'], url=self.url, headers=self.headers)
        soup = BeautifulSoup(self.r.text, 'html.parser')
        first_row = soup.find('tr', class_='grid-row')
        self.assertIsNotNone(first_row, "Search Result is Null，no record for tr.grid-row")
        all_tds = first_row.find_all('td')
        actual_quote_no = all_tds[1].get_text().strip()
        print('actual_quote is: ',actual_quote_no)
        self.assertEqual(self.data[7]['response'], actual_quote_no)

    def test_api_05(self):
        """Verify Verify Door type on Quotation screen"""
        endpoint = self.data[9]['Endpoint']
        self.url = self.base_url + endpoint
        self.r = self.session.request(method=self.data[15]['method'], url=self.url, headers=self.headers)
        soup = BeautifulSoup(self.r.text, 'html.parser')
        target_span_or_td = soup.find(string=lambda text: text and 'Door Type:' in text)
        self.assertIsNotNone(target_span_or_td, "can't find any 'Door Type:' in the response.")
        next_td = target_span_or_td.parent.find_next_sibling()
        actual_door_type = next_td.get_text().strip()
        print("Captured Door Type is:", actual_door_type)
        self.assertEqual(self.data[15]['response'], actual_door_type)

    def test_api_06(self):
        """Verify Verify No. of Handsets on Quotation screen"""
        endpoint = self.data[9]['Endpoint']
        self.url = self.base_url + endpoint
        self.r = self.session.request(method=self.data[30]['method'], url=self.url, headers=self.headers)
        soup = BeautifulSoup(self.r.text, 'html.parser')
        text_node = soup.find(string=re.compile(r'No. of Handsets:'))
        self.assertIsNotNone(text_node,
                             "Can't find 'No. of Handsets:'，please check the response")
        target_div = text_node.find_parent('div', class_='col-md-4')
        full_text = target_div.get_text().strip()
        print("Captured Full Text is:", full_text)
        actual_handsets = re.sub(r'No. of Handsets:\s*', '', full_text, flags=re.IGNORECASE).strip()
        print("Cleaned No. of Handsets is:", actual_handsets)
        self.assertEqual(str(self.data[30]['response']),actual_handsets)

if __name__ == '__main__':
    unittest.main(verbosity=2)








































