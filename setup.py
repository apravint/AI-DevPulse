from setuptools import setup, find_packages

setup(
    name="ai-devpulse",
    version="1.0.0",
    description="Autonomous AI Code Reviewer, Vulnerability Scanner & Refactoring Agent CLI",
    author="Ayyappa Pravin",
    author_email="apravint@gmail.com",
    url="https://github.com/apravint/AI-DevPulse",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "devpulse=devpulse.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
