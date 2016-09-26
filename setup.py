from setuptools import setup


setup(
    name='pyknowsis',
    include_package_data=True,
    version="0.1.5",
    packages=[
        'pyknowsis',
        'tests'
    ],
    description='API Wrapper for the Knowsis API',
    author='Knowsis Ltd',
    author_email='mark@knowsis.com',
    dependency_links=[],
    install_requires=['requests', 'simplejson', 'oauth2', 'python-dateutil'],
    tests_require=[],
    url="https://github.com/knowsis/pyknowsis",
    download_url='https://github.com/knowsis/pyknowsis/tarball/0.1.5',
)
