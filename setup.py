import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

module_name = 'contract_watcher'

module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()


class LoadException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


def load_requirements(file_name: str) -> list:
    requirements = []

    with open(file_name, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


requirements_txt = '/requirements.txt'

setup(
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements(requirements_txt),
    include_package_data=True,
    entry_points={
            'console_scripts': [
                '{0} = {0}.__main__:cli'.format(module_name),
                'cw-daemon = {0}.daemon.__main__:run'.format(module_name)
            ]
        },
)
