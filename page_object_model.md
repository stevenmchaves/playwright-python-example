Page object models
==================

A page object represents a part of your web application using a page, alert, popup, etc. 
An e-commerce web application might have a home page, a listings page and a checkout page. Each of them can be represented by page object models.

Page objects simplify authoring by creating a higher-level API which suits your application and simplify maintenance by capturing element selectors in one place and create reusable code to avoid repetition.

# Implementation
Page object models wrap over a Playwright Page.

```
models/search.py
class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_term_input = page.locator('[aria-label="Enter your search term"]')

    async def navigate(self):
        await self.page.goto("https://bing.com")

    async def search(self, text):
        await self.search_term_input.fill(text)
        await self.search_term_input.press("Enter")
```

Page objects can then be used inside a test.
NOW USE IT IN THE TEST:

```
test_search.py
from models.search import SearchPage

# in the test
page = await browser.new_page()
search_page = SearchPage(page)
await search_page.navigate()
await search_page.search("search query")
```