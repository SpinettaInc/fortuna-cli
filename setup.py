from setuptools import setup

setup(
    name='fortuna',
    version='1.0',
    description='Fortuna CLI setup',
    author='Benjamin Lo',
    author_email='benjaminlouk011@gmail.com',
    install_requires=['pyfiglet', 'PyInquirer'],
    entry_points={
        'console_scripts': [
            'fortuna = fortuna:main',
        ],
    }
)
