import setuptools, sys

setuptools.setup(
    name="watchdog-tricks",
    version='0.1.1',
    license="MIT",

    author="Ryan Ye",
    author_email="yejianye@gmail.com",
    url="https://github.com/yejianye/watchdog-tricks",

    description="Common tricks for watchdog (Python file system monitoring tool), including watcher for LessCss, CoffeeScript etc",
    long_description=open("README.md").read(),
    keywords=["watchdog","watcher","tricks"],
    classifiers=[
            "Environment :: Console",
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Environment :: Other Environment",
            "Topic :: Utilities",
            "Topic :: System :: Monitoring",
            "Topic :: System :: Filesystems",
        ],
    entry_points={
        'console_scripts': [
            'lesswatcher = watchdog_tricks.lesswatcher:main',
            'ctagswatcher = watchdog_tricks.ctagswatcher:main',
        ]
    },
    install_requires=['watchdog'],
    packages=['watchdog_tricks'],
)
