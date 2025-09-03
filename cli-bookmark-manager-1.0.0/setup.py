"""
Setup script for CLI Bookmark Manager
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cli-bookmark-manager",
    version="1.0.0",
    author="Ersin KOÇ",
    author_email="ersinkoc@gmail.com",
    description="A powerful command-line bookmark manager built with Python and SQLite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ersinkoc/bookmark-manager",
    project_urls={
        "Bug Tracker": "https://github.com/ersinkoc/bookmark-manager/issues",
        "Documentation": "https://github.com/ersinkoc/bookmark-manager/blob/main/README.md",
        "Source Code": "https://github.com/ersinkoc/bookmark-manager",
        "Changelog": "https://github.com/ersinkoc/bookmark-manager/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Utilities",
        "Topic :: Text Processing :: Markup :: HTML",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "build>=0.8.0",
            "twine>=4.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "requests-mock>=1.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bookmark-manager=bookmark_manager.main:main",
            "bm=bookmark_manager.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "bookmark_manager": [
            "*.bat",
            "*.py",
            "*.md",
        ],
    },
    zip_safe=False,
    keywords="bookmark manager cli command-line sqlite organizer utility",
    license="MIT",
)