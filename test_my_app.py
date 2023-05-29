import pytest
import re
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    print("beforeEach")
    # Go to the starting url before each test.
    page.goto("https://playwright.dev/")
    yield
    print("afterEach")

def test_main_navigation(page: Page):
    # Assertions use the expect API.
    expect(page).to_have_url("https://playwright.dev/")
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))




def test_example(page: Page) -> None:
    page.goto("https://demo.playwright.dev/todomvc/")
    page.get_by_placeholder("What needs to be done?").click()
    page.get_by_placeholder("What needs to be done?").fill("Hello")
    page.get_by_placeholder("What needs to be done?").press("Enter")
    page.get_by_placeholder("What needs to be done?").fill("Yes it was correct")
    page.get_by_placeholder("What needs to be done?").press("Enter")
    page.get_by_role("link", name="Completed").click()
    page.get_by_role("link", name="All").click()
    page.get_by_role("listitem").filter(has_text="Yes it was correct").get_by_role("checkbox", name="Toggle Todo").check()
    page.get_by_role("link", name="Completed").click()
    page.get_by_role("link", name="Active").click()
    page.get_by_role("link", name="Completed").click()
    page.get_by_role("button", name="Clear completed").click()
    page.get_by_role("link", name="All").click()
    page.get_by_test_id("todo-title").click()
    page.get_by_role("checkbox", name="Toggle Todo").check()
    page.get_by_role("link", name="Active").click()
    page.get_by_role("link", name="real TodoMVC app.").click()


def test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(page: Page):
    
    # create a locator
    get_started = page.get_by_role("link", name="Get started")

    # Expect an attribute "to be strictly equal" to the value.
    expect(get_started).to_have_attribute("href", "/docs/intro")

    # Click the get started link.
    get_started.click()

    # Expects the URL to contain intro.
    expect(page).to_have_url(re.compile(".*intro"))
    


def test_homepage_get_started_link_linking_to_the_intro_page(page: Page):
    # create a locator
    get_started = page.get_by_role("link", name="Get started")
    get_started.click()
    #docusaurus_skipToContent_fallback > div > aside > div > div > nav > ul > li:nth-child(1) > ul > li:nth-child(1) > a
    expect(page.get_by_role("link", name="Installation")).to_be_visible()

    # Expects the URL to contain intro.
    expect(page).to_have_url(re.compile(".*intro"))