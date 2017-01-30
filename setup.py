from setuptools import setup, find_packages
# To use a consistent encoding

setup(
    name = 'gh-notifier',

    version = '0.1.0',

    description = "A Desktop notifier for all your social GitHub notifications",

    url = "https://github.com/kshitij10496/gh-notifier",
    author='Kshitij Saraogi',
    author_email='KshitijSaraogi@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords='github',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['requests'],

    entry_points={
        'console_scripts': [
            'gh-notifier=ghnotifier.main_cli:main',
        ],
    },
)
