Notes
=======

Pages
--------
- Pages
- Multiple pages
- Handling new pages
- Handling popups

# Pages
Each BrowserContext can have multiple pages. A Page refers to a single tab or a popup window within a browser context. It should be used to navigate to URLs and interact with the page content.

```
page = await context.new_page()

# Navigate explicitly, similar to entering a URL in the browser.
await page.goto('http://example.com')
# Fill an input.
await page.locator('#search').fill('query')

# Navigate implicitly by clicking a link.
await page.locator('#submit').click()
# Expect a new url.
print(page.url)
```

# Multiple pages
Each browser context can host multiple pages (tabs).

Each page behaves like a focused, active page. Bringing the page to front is not required.
Pages inside a context respect context-level emulation, like viewport sizes, custom network routes or browser locale.

```
# create two pages
page_one = await context.new_page()
page_two = await context.new_page()

# get pages of a browser context
all_pages = context.pages
```

# Handling new pages
The page event on browser contexts can be used to get new pages that are created in the context. This can be used to handle new pages opened by target="_blank" links.

```
# Get page after a specific action (e.g. clicking a link)
async with context.expect_page() as new_page_info:
    await page.get_by_text("open new tab").click() # Opens a new tab
new_page = await new_page_info.value

await new_page.wait_for_load_state()
print(await new_page.title())
```

If the action that triggers the new page is unknown, the following pattern can be used.

```
# Get all new pages (including popups) in the context
async def handle_page(page):
    await page.wait_for_load_state()
    print(await page.title())

context.on("page", handle_page)
```

# Handling popups
If the page opens a pop-up (e.g. pages opened by target="_blank" links), you can get a reference to it by listening to the popup event on the page.

This event is emitted in addition to the browserContext.on('page') event, but only for popups relevant to this page.

```
# Get popup after a specific action (e.g., click)
async with page.expect_popup() as popup_info:
    await page.get_by_text("open the popup").click()
popup = await popup_info.value

await popup.wait_for_load_state()
print(await popup.title())
```

If the action that triggers the popup is unknown, the following pattern can be used.

```
# Get all popups when they open
async def handle_popup(popup):
    await popup.wait_for_load_state()
    print(await popup.title())

page.on("popup", handle_popup)
```

Screenshots
------------

```
await page.screenshot(path="screenshot.png")
```
Screenshots API accepts many parameters for image format, clip area, quality, etc. Make sure to check them out.

- Full page screenshots
- Capture into buffer
- Element screenshot

# Full page screenshots
Full page screenshot is a screenshot of a full scrollable page, as if you had a very tall screen and the page could fit it entirely.

```
await page.screenshot(path="screenshot.png", full_page=True)
```

# Capture into buffer
Rather than writing into a file, you can get a buffer with the image and post-process it or pass it to a third party pixel diff facility.

```
# Capture into Image
screenshot_bytes = await page.screenshot()
print(base64.b64encode(screenshot_bytes).decode())
```

# Element screenshot

Sometimes it is useful to take a screenshot of a single element.

```
await page.locator(".header").screenshot(path="screenshot.png")
```


Test generator
---------------
Generate tests for you as you perform actions in the browser and is a great way to quickly get started with testing. Playwright will look at your page and figure out the best locator, prioritizing role, text and test id locators. If the generator finds multiple elements matching the locator, it will improve the locator to make it resilient that uniquely identify the target element.

# Generate tests with the Playwright Inspector
When running the codegen command two windows will be opened, a browser window where you interact with the website you wish to test and the Playwright Inspector window where you can record your tests and then copy them into your editor.

## Running Codegen
Use the codegen command to run the test generator followed by the URL of the website you want to generate tests for. The URL is optional and you can always run the command without it and then add the URL directly into the browser window instead.
```
playwright codegen demo.playwright.dev/todomvc
```
## Recording a test
Run the codegen command and perform actions in the browser window. Playwright will generate the code for the user interactions which you can see in the Playwright Inspector window. Once you have finished recording your test stop the recording and press the *copy* button to copy your generated test into your editor.


## Generating locators
You can generate locators with the test generator.

- Press the 'Record' button to stop the recording and the 'Pick Locator' button will appear.
- Click on the 'Pick Locator' button and then hover over elements in the browser window to see the locator highlighted underneath each element.
- To choose a locator click on the element you would like to locate and the code for that locator will appear in the field next to the Pick Locator button.
- You can then edit the locator in this field to fine tune it or use the copy button to copy it and paste it into your code.

# Emulation
You can use the test generator to generate tests using emulation so as to generate a test for a specific viewport, device, color scheme, as well as emulate the geolocation, language or timezone. The test generator can also generate a test while preserving authenticated state.

## Emulate viewport size
Playwright opens a browser window with it's viewport set to a specific width and height and is not responsive as tests need to be run under the same conditions. Use the `--viewport` option to generate tests with a different viewport size.
```
playwright codegen --viewport-size=800,600 playwright.dev
```
Codegen generating code for tests for playwright.dev website with a specific viewport python

## Emulate devices
Record scripts and tests while emulating a mobile device using the `--device` option which sets the viewport size and user agent among others.
```
playwright codegen --device="iPhone 13" playwright.dev
```
Codegen generating code for tests for `playwright.dev` website emulated for iPhone 13 python

## Emulate color scheme
Record scripts and tests while emulating the color scheme with the `--color-scheme` option.
```
playwright codegen --color-scheme=dark playwright.dev
```
Codegen generating code for tests for `playwright.dev` website in dark mode python
## Emulate geolocation, language and timezone
Record scripts and tests while emulating timezone, language & location using the `--timezone`, `--geolocation` and `--lang` options. Once the page opens:

1. Accept the cookies
2. On the top right click on the locate me button to see geolocation in action.
```playwright codegen --timezone="Europe/Rome" --geolocation="41.890221,12.492348" --lang="it-IT" bing.com/maps
```
Codegen generating code for tests for bing maps showing timezone, geolocation as Rome, Italy and in Italian language python

## Preserve authenticated state
Run codegen with `--save-storage` to save *cookies* and *localStorage* at the end of the session. This is useful to separately record an authentication step and reuse it later when recording more tests.
```
playwright codegen github.com/microsoft/playwright --save-storage=auth.json
```

### Login
After performing authentication and closing the browser, `auth.json` will contain the storage state which you can then reuse in your tests.

Make sure you only use the `auth.json` locally as it contains sensative information. Add it to your `.gitignore` or delete it once you have finished generating your tests.

### Load authenticated state
Run with --load-storage to consume the previously loaded storage from the auth.json. This way, all cookies and localStorage will be restored, bringing most web apps to the authenticated state without the need to login again. This means you can can continue generating tests from the logged in state.
```
playwright codegen --load-storage=auth.json github.com/microsoft/playwright
```

# Record using custom setup
If you would like to use codegen in some non-standard setup (for example, use browser_context.route()), it is possible to call page.pause() that will open a separate window with codegen controls.
```
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Make sure to run headed.
        browser = await p.chromium.launch(headless=False)

        # Setup context however you like.
        context = await browser.new_context() # Pass any options
        await context.route('**/*', lambda route: route.continue_())

        # Pause the page, and start recording manually.
        page = await context.new_page()
        await page.pause()

asyncio.run(main())
```

Videos
-------
Playwright has the capabilities of recording videos of tests.

# Record video
Videos are saved upon browser context closure at the end of a test.

*Sync*
```
context = browser.new_context(record_video_dir="videos/")
# Make sure to close, so that videos are saved.
context.close()
```
*Async*
```
context = await browser.new_context(record_video_dir="videos/")
# Make sure to await close, so that videos are saved.
await context.close()
```

Default video size is 800x800, but can be modified. 

*Sync*
```
context = browser.new_context(
    record_video_dir="videos/",
    record_video_size={"width": 640, "height": 480}
)
```
*Async*
context = browser.new_context(
    record_video_dir="videos/",
    record_video_size={"width": 640, "height": 480}
)

Saved video files will appear in the specified folder. They all have generated unique names. For the multi-page scenarios, you can access the video file associated with the page via the page.video.

*Sync*
`path = page.video.path()`
*Async*
`path = await page.video.path()`

*Videos are available after the page or browser context are closed.*


Trace viewer
--------------
GUI tool that helps you explore recorded Playwright traces after the script has ran. You can open traces locally or in your browser on `trace.playwright.dev`.

# Viewing the trace
You can open the saved trace using Playwright CLI or in your browser on `trace.playwright.dev`.

```
playwright show-trace trace.zip
```

## Actions
Once trace is opened, you will see the list of actions Playwright performed on the left hand side.

*Selecting each action reveals:*

- action snapshots,
- action log,
- source code location,
- network log for this action

In the properties pane you will also see rendered DOM snapshots associated with each action.

## Metadata
See metadata such as the time the action was performed, what browser engine was used, what the viewport was and if it was mobile and how many pages, actions and events were recorded.

## Screenshots
When tracing with the `screenshots` option turned on, each trace records a screencast and renders it as a film strip.

You can hover over the film strip to see a magnified image of for each action and state which helps you easily find the action you want to inspect.

## Snapshots
When tracing with the snapshots option turned on, Playwright captures a set of complete DOM snapshots for each action. Depending on the type of the action, it will capture:

|  Type  |	Description
|--------|------------------------------------------|
| Before | A snapshot at the time action is called. |
| Action | A snapshot at the moment of the performed input. This type of snapshot is especially useful when exploring where exactly Playwright clicked. |
| After  | A snapshot after the action. |

## Call
See what action was called, the time and duration as well as parameters, return value and log.

## Console
See the console output for the action where you can see console logs or errors.

## Network
See any network requests that were made during the action.

## Source
See the source code for your entire test.

## Recording a trace
Traces can be recorded using the browser_context.tracing API as follows:

```
browser = await chromium.launch()
context = await browser.new_context()

# Start tracing before creating / navigating a page.
await context.tracing.start(screenshots=True, snapshots=True, sources=True)

await page.goto("https://playwright.dev")

# Stop tracing and export it into a zip archive.
await context.tracing.stop(path = "trace.zip")
```

The above snippet will record the trace and place it into the file named `trace.zip`.

## Viewing the trace
You can open the saved trace using Playwright CLI or in your browser on `trace.playwright.dev`.
```
playwright show-trace trace.zip
```
## Using trace.playwright.dev
trace.playwright.dev is a statically hosted variant of the Trace Viewer. You can upload trace files using drag and drop.

Drop Playwright Trace to load
## Viewing remote traces
You can open remote traces using it's URL. They could be generated on a CI run which makes it easy to view the remote trace without having to manually download the file.
```
playwright show-trace https://example.com/trace.zip
```
You can also pass the URL of your uploaded trace (e.g. inside your CI) from some accessible storage as a parameter. CORS (Cross-Origin Resource Sharing) rules might apply.
```
https://trace.playwright.dev/?trace=https://demo.playwright.dev/reports/todomvc/data/cb0fa77ebd9487a5c899f3ae65a7ffdbac681182.zip
```




