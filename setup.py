"""
Setup script for ZapCards - AI-Powered Study Companion
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="zapcards",
    version="1.0.0",
    author="ZapCards Contributors",
    author_email="support@zapcards.app",
    description="AI-Powered Study Companion with 8 Aesthetic Themes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/zapcards",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "zapcards=main:main",
        ],
    },
    keywords="quiz study ai education flashcards learning",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/zapcards/issues",
        "Source": "https://github.com/yourusername/zapcards",
        "Documentation": "https://github.com/yourusername/zapcards#readme",
    },
)