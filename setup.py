import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NuInfoSys",
    version="1.0.0",
    author="Adam Brewer",
    author_email="adamhb321@gmail.com",
    description="NuInfoSys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adamhb123/NuInfoSys",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "./"},
    packages=setuptools.find_packages(where="./"),
    python_requires=">=3.6",
)
