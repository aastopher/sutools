import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sutools",
    version="0.1.2",
    author="Aaron Stopher",
    packages=setuptools.find_packages(include=["sutools"]),
    description="su (Super User) tools; per module utilities, designed to be lightweight, easy to configure, and reduce boilerplate code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aastopher/sutools",
    project_urls={
        "Documentation": "https://sutools.readthedocs.io",
        "Bug Tracker": "https://github.com/aastopher/sutools/issues",
    },
    keywords=['logs', 'logger', 'logging', 'cli', 'utils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
