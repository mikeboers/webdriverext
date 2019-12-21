from webdriverext import Chrome
from webdriverext.utils import jprint

driver = Chrome()

url = 'https://httpbin.org/get?foo=bar'
driver.get(url)

id_ = driver.download(url)
print(id_)

jprint(driver.get_downloads())


