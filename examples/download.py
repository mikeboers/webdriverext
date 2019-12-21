from webdriverext import Chrome
from webdriverext.utils import jprint


driver = Chrome()

# Prime it.
driver.get('https://httpbin.org/get')

download = driver.download('https://httpbin.org/drip?duration=1&numbytes=1000&delay=0')
print(download)
print(download.wait())
print(driver.get_downloads())
jprint(download.data)
print(download.filename)
print(download.start_time)