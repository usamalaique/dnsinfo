from setuptools import setup, find_packages

setup(
    name='dnsinfo',
    version='0.1',
    py_modules=['dnsinfo'],
    install_requires=[
        'dnspython',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'dnsinfo=dnsinfo:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool to gather DNS information',
    url='https://github.com/yourusername/dnsinfo',
    python_requires='>=3.6',
)
