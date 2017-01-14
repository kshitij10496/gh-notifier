from setuptools import setup, find_packages
# To use a consistent encoding

setup(
    name = 'gh-notifier',

    version = '0.0.1',

    description = "A Desktop notifier for all your social GitHub notifications."

    url = "https://github.com/kshitij10496/gh-notifier"
    author='Kshitij Saraogi',
    author_email='KshitijSaraogi@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools :: GitHub',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords='github',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['requests', 'PyGitHub', 'bs4'],

    entry_points={
        'console_scripts': [
            'gh-notifier=gh-notifier:main_cli:main',
        ],
    },
)
