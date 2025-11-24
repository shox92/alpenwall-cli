from setuptools import setup, find_packages

setup(
    name='alpenwall-cli',
    description='Command-line interface for AlpenWall',
    version='0.1.4',
    url='https://github.com/shox92/alpenwall-cli.git',
    author='Tim Fehmer',
    author_email='kontakt@alpenwall.at',
    entry_points={
        'console_scripts': [
            'alpenwall-cli = cli.app:AlpenWallApp.run',
        ],
    },
    packages=find_packages(),
    setup_requires=[],
    install_requires=[
        'plumbum==1.6.9',
    ],
    test_suite='tests.test_alpenwall-cli',
    keywords=['alpenwall']
)
