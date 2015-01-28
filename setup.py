from setuptools import setup
from knowsis import version

from pip.req import parse_requirements


install_requirements = [str(ir.req) for ir in parse_requirements('requirements.txt')]
test_requirements = [str(ir.req) for ir in parse_requirements('requirements-testing.txt')]


setup(
    name='pyknowsis',
    include_package_data=True,
    version=version,
    packages=[
        'pyknowsis',
    ],
    description='API Wrapper for the Knowsis API',
    author='Knowsis Ltd',
    dependency_links=[],
    install_requires=install_requirements,
    tests_require=test_requirements,
    url="https://github.com/knowsis/pyknowsis"
)
