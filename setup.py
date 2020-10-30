from setuptools import setup, find_packages

long_description = ""
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="brigadier.py",
    description="Implementation of Mojang's brigadier in Python",
    version="1.0.0",
    author="thelennylord",
    packages=find_packages(),
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thelennylord/brigadier.py",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.7"
)