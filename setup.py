from setuptools import setup, find_packages

setup(
    name='pyscan-tool',
    version='0.1',
    description='A CLI tool for network port scanning',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hatix Ntsoa',
    author_email='hatixntsoa@gmail.com',
    url='https://github.com/h471x/port_scanner',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyscan=pyscan.main:main',
        ],
    },
)