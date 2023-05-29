CI
====

1. Ensure you have an environment that can run the playwright CLI.

2. Install playwright
```
pip install playwright
playwright install --with-deps
```
3. Run your tests `pytest`

# CI Configurations

1. GitHub Actions
    - on push/pull_request
    - via containers
    - on deployment

2. Docker
3. Azure Pipelines
4. CircleCI
5. Jenkins
6. Bitbucket Pipelines
7. GitLab CI

# Caching browsers
Default behavior is to download browser binaries to certain directoris based on OS. If caching is desired, cache the specific location of your browser in the CI configuration against a hash of the playwright version.
- learn what is meant by this

# Running headed
`headless=False`
Linux agents requires Xvfb to be insealled. Using the playwright Docker image this is already installed.
`xvfb-run python test.py`