from setuptools import setup, find_packages

setup(
    name='mistborn-cli',
    description='Command-line interface for Stormblest Mistborn',
    version='2.0.1',
    url='https://gitlab.com/cyber5k/mistborn-cli.git',
    author='Steven Foerster',
    author_email='steven@stormblest.com',
    entry_points={
        'console_scripts': [
            'mistborn-cli = cli.app:MistbornApp.run',
        ],
    },
    packages=find_packages(),
    setup_requires=[],
    install_requires=[
        'plumbum==1.6.9',
        'Jinja2==3.1.2',
    ],
    test_suite='tests.test_mistborn-cli',
    keywords=['mistborn']
)
