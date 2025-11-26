from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="greenpipeline",
    version="0.1.0",
    author="GreenPipeline Team",
    author_email="info@greenpipeline.dev",
    description="Framework para medir y reducir la huella de carbono en CI/CD pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greenpipeline/framework",
    project_urls={
        "Bug Tracker": "https://github.com/greenpipeline/framework/issues",
        "Documentation": "https://docs.greenpipeline.dev",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "psutil>=5.9.0",
        "requests>=2.28.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
        ],
        "dashboard": [
            "flask>=2.3.0",
            "plotly>=5.14.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "greenpipeline=greenpipeline.cli:main",
        ],
    },
)
