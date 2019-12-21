from webdriverext import Chrome


driver = Chrome()

print(driver.post('https://httpbin.org/post', dict(foo='bar')))
