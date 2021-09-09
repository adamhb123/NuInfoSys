import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NuInfoSys",
    version="0.0.1",
    author="Adam Brewer",
    author_email="adamhb321@gmail.com",
    description="NuInfoSys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adamhb123/NuInfoSys",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=["NuInfoSys"]),
    python_requires=">=3.6",
)
