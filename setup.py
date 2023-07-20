import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BuoyanText",
    version="0.0.5",
    author="Boyang Xu",
    author_email="by24225@163.com",
    description="Normalizing English and Chinese Text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BuoyantXu/BuoyantText",
    install_requires=[
        "setuptools>=61.0",
        "pymupdf",
        "pandas",
        "nltk",
        "jieba",
        "spacy",
        "bs4",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/BuoyantXu/BuoyantText/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
    ],
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"BuoyanText": ["data/norm/*.json"]},
    python_requires=">=3.7",
)
