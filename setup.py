from setuptools import setup


setup(
    name='pyknowsis',
    include_package_data=True,
    version="0.1.4.1",
    packages=[
        'pyknowsis',
        'tests'
    ],
    description='API Wrapper for the Knowsis API',
    author='Knowsis Ltd',
    author_email='mark@knowsis.com',
    dependency_links=[],
    install_requires=['requests', 'simplejson', 'oauth2'],
    tests_require=[],
    url="https://github.com/knowsis/pyknowsis"
)
