from setuptools import setup, find_packages

setup(
    name='mistborn-cli',
    description='Command-line interface for Cyber5K Mistborn',
    version='0.1',
    url='https://gitlab.com/cyber5k/mistborn-cli.git',
    author='Steven Foerster',
    author_email='steven@cyber5k.com',
    entry_points={
        'console_scripts': [
            'mistborn-cli = cli.app:MistbornApp.run',
        ],
    },
    packages=find_packages(),
    setup_requires=[],
    install_requires=[
        'plumbum==1.6.9',
    ],
    test_suite='tests.test_mistborn',
    keywords=['mistborn']
)
