from setuptools import setup, find_packages

setup(
    name='multi_opc',
    version='0.0.1',
    author='Mark Feldhousen',
    author_email='markf+opcu@geekpad.com',
    packages=['opc'],
    include_package_data=True,
    zip_safe=False,
    #scripts=['bin/foo'],
    entry_points={
        'console_scripts': [
          'multi_opc=opc.multi_opc:main',
        ],
    },
    license='LICENSE.txt',
    description='Multi Open Pixel Controller',
    long_description=open('README.md').read(),
    install_requires=[
        "docopt >= 0.6.2",
        "PyYAML >= 3.12",
        "watchdog >= 0.8.3"
    ]
)
