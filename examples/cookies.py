from webdriverext import Chrome
from webdriverext.utils import jprint


driver = Chrome()

driver.get('https://httpbin.org/cookies/set/foo/bar')

jprint(driver.get_cookies())

