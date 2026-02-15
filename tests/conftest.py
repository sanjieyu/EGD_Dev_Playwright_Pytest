# Author:Yi Sun(Tim) 2024-1-22


import pytest
import os

# 1. Creat a page
@pytest.fixture(scope="class")
def page_in_class(browser, browser_context_args):
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    yield page
    context.close()
# status file path
AUTH_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../auth.json"))

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, credentials):

    if os.path.exists(AUTH_PATH):
        return {
            **browser_context_args,
            "storage_state": AUTH_PATH,
            "viewport": {"width": 2560, "height": 1440}
        }
    return {
        **browser_context_args,
        "viewport": {"width": 2560, "height": 1440}
    }


@pytest.fixture(scope="session", autouse=True)
def auto_login_setup(browser, credentials):

    should_login = False
    if not os.path.exists(AUTH_PATH):
        should_login = True
        print("\n[Auth] Can't find auth.json，run login...")

    else:
        # Re-authenticate if the token/file is expired (over 24 hours).
        file_age = time.time() - os.path.getmtime(AUTH_PATH)
        if file_age > 86400:    # 24 hours
            print("\n[Auth] auth.json is expired (over 24 hours),prpare to re-login...")
            should_login = True

    if should_login:
        print("\n[Auth] start to login from UI...")
        context = browser.new_context()
        page = context.new_page()

        try:
            from pages.login_admin import Admin_Portal
            admin = Admin_Portal(page)
            page.goto(credentials["egd_url"])
            admin.login(credentials["admin_username"],credentials["admin_password"])
            page.wait_for_load_state("networkidle")

            # save login credentials
            context.storage_state(path=AUTH_PATH)
            print(f"[Auth] login successfully, credentials saved to: {AUTH_PATH}")
        except Exception as e:
            pytest.exit(f"[Auth] Login fail, error: {e}")
        finally:
            context.close()
    else:
        print("\n[Auth] Login credentials already exists, skip the UI login steps.")
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = None

        if "page" in item.funcargs:
            page = item.funcargs["page"]
        else:
            for fixture_value in item.funcargs.values():
                if hasattr(fixture_value,"page"):
                    page = fixture_value.page
                    break
        if page:
            screenshot_dir = os.path.join("Report", "screenshots")
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            safe_name = "".join([c for c in item.name if c.isalnum() or c in (' ', '.', '_')]).rstrip()
            img_path = os.path.join(screenshot_dir, f"{safe_name}.png")
            try:
                page.screenshot(path=img_path, full_page=True)
                print(f"\n[Screenshot] get the snapthos: {img_path}")
            except Exception as e:
                print(f"\n[Screenshot] get snapshot fail: {e}")

@pytest.fixture(scope="class")
def dealer_page(browser, credentials):
    context = browser.new_context()
    page = context.new_page()
    page.goto(credentials["egd_url"])
    yield page
    context.close()




