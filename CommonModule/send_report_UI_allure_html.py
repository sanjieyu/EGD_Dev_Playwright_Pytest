# Author:Yi Sun(Tim) 2024-9-01

'''Automation Test Report'''

import pytest
import time
import os
import smtplib
import subprocess
import shutil
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
import zipfile
import tempfile
import allure
from allure_pytest import plugin as allure_plugin

class SendReportUI:
    def new_report_ui(self,test_report):
        """Get the allure report dictionary"""
        if not os.path.exists(test_report):
            os.makedirs(test_report)
        reports = [d for d in os.listdir(test_report)  if os.path.isdir(os.path.join(test_report,d))]
        if not reports:
            return None

        reports.sort(key=lambda fn:os.path.getmtime(os.path.join(test_report,fn)))
        latest_report = os.path.join(test_report,reports[-1])
        print(f"Latest report directory: {latest_report}")
        return latest_report

    def generate_allure_report(self,allure_results_dir, allure_report_dir):
        """Generate Allure HTML report"""
        allure_path = r"C:\allure\bin\allure.bat"

        if not os.path.exists(allure_report_dir):
            os.makedirs(allure_report_dir)

        cmd = [allure_path, "generate", allure_results_dir, "-o", allure_report_dir, "--clean", "--single-file"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print("Allure report generation command executed.")
            if result.returncode == 0:
                print("✅ Allure report generated successfully with --single-file parameter")
                print(f"Output: {result.stdout}")

                # Verify the file size
                index_html_path = os.path.join(allure_report_dir, "index.html")
                if os.path.exists(index_html_path):
                    file_size = os.path.getsize(index_html_path)
                    print(f"Report file size: {file_size / (1024 * 1024):.2f} MB")
                    if file_size > 100000:
                        return True
                    else:
                        print("⚠️ Report file might still be too small")
                        return False
                else:
                    print("❌ index.html not found")
                    return False
            else:
                print(f"❌ Allure command failed with return code: {result.returncode}")
                print(f"STDERR: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ Allure command timed out")
            return False
        except Exception as e:
            print(f"❌ Error generating Allure report: {e}")
            return False

    def copy_rename_report(self, report_dir):
        try:
            source_report_file = os.path.join(report_dir, "index.html")
            if not os.path.exists(source_report_file):
                print(f"❌ Source Report file not found: {source_report_file}")
                return None
            parent_dir = os.path.dirname(report_dir)
            timestamp = time.strftime("%Y-%m-%d_%H_%M_%S")
            new_report_name = f"UI_Automation_Report_{timestamp}.html"
            target_report_file = os.path.join(parent_dir, new_report_name)
            shutil.copy(source_report_file, target_report_file)
            print(f"copied to {target_report_file}")
            return target_report_file
        except Exception as e:
            print(f"❌ Error copying report: {e}")
            return None

    def send_mail_ui(self,html_report_path):
        """Send email with report attached"""
        sender = 'egdautomation@xxx'
        receiver = ['aaaa@xxxx.com.au', 'bbbb@xxxx.com.au', 'xxxx@xxxx.com.au']
        subject = 'UI Automation Test Report for EGD'
        msg = MIMEMultipart('mixed')
        body_text = f'''Automation Test completed at {time.strftime("%Y-%m-%d %H:%M:%S")}. The detailed test report is 
        attached as HTML file. Please open the attached HTML file to view the full report.DO NOT reply. Thank you!'''
        msg_html1 = MIMEText(body_text, 'plain', 'utf-8')
        msg.attach(msg_html1)

        if html_report_path and os.path.exists(html_report_path):
            try:
                with open(html_report_path, 'rb') as f:
                    html_content = f.read()
                html_attachment = MIMEText(html_content, 'html', 'utf-8')
                html_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(html_report_path)
                )
                msg.attach(html_attachment)
                print(f"✅ HTML report attached: {os.path.basename(html_report_path)}")
            except Exception as e:
                print(f"❌ Error attaching HTML file: {e}")

        msg['From'] = sender
        msg['To'] = ";".join(receiver)
        msg['Subject'] = Header(subject, 'utf-8')

        try:
            smtpserver = 'smtp.gmail.com'
            smtp = smtplib.SMTP(smtpserver, 587)
            smtp.ehlo()
            smtp.starttls()
            print('Connected to SMTP server successfully!')
            user = 'egdautomation@xxxx.com'
            password = 'xxxxxxx'
            smtp.login(user, password)
            print('Start to send')
            smtp.sendmail(sender, receiver, msg.as_string())
            print('Mail sent successfully!')
            smtp.quit()
        except smtplib.SMTPException as e:
            print('Mail send error:', e)
        except Exception as e:
            print('Unexpected error:', e)

def run_tests_and_send_report():
    test_dir_ui = "xxxxx\\UITestCase"
    allure_results_dir = "xxxxx\\Report\\UI\\allure-results"
    allure_report_dir = "xxxxx\\Report\\UI\\allure-report"

    os.makedirs(allure_results_dir, exist_ok=True)
    os.makedirs(allure_report_dir, exist_ok=True)
    report_sender = SendReportUI()

    print("Starting pytest tests...")
    pytest_args = [
        test_dir_ui,
        f"--alluredir={allure_results_dir}",
        "-v",
        "--tb=short"
    ]
    exit_code = pytest.main(pytest_args)
    print(f"Tests completed with exit code: {exit_code}")

    # Generate report
    print("Generating Allure report...")
    success = report_sender.generate_allure_report(allure_results_dir, allure_report_dir)
    if success:
        renamed_report_path = report_sender.copy_rename_report(allure_report_dir)
        if renamed_report_path:
            print("Sending email with HTML attachment...")
            report_sender.send_mail_ui(renamed_report_path)
        else:
            print("❌ Failed to copy and rename report file, email not sent")
    else:
        print("❌ Failed to generate Allure report, email not sent")


if __name__ == "__main__":
    run_tests_and_send_report()


