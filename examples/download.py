from webdriverext import Chrome


driver = Chrome()

# Prime it.
driver.get('https://httpbin.org/get')

download = driver.download('https://httpbin.org/drip?duration=2&numbytes=1000&delay=0')
print(download)
print(download.wait())
print(driver.get_downloads())
print(download.filename)
