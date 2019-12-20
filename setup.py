from distutils.core import setup

setup(

    name='webdriverext',
    version='1.0.0.dev0',
    description='WebDriver extensions.',
    url='http://github.com/mikeboers/webdriverext',
    
    packages=['webdriverext'],
    
    author='Mike Boers',
    author_email='webdriverext@mikeboers.com',
    license='BSD-3',

    install_requires='''
        lxml
        requests
        selenium
    ''',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    
)
