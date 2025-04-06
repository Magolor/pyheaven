cp -rf ./.pypirc ~/.pypirc
echo 'from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.1.6.8"
with open("__init__.py", "w") as f:
    f.write(f"__version__ = \"{VERSION}\"")

setup(
    name = "pyheaven",
    version = VERSION,
    author = "Magolor",
    author_email = "magolorcz@gmail.com",
    description = "Python Heaven",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/Magolor/",
    project_urls={
        "Author":"https://github.com/Magolor/",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
)' > setup.py
sh installer.sh
# python setup.py sdist upload
pdoc -d google --output-dir doc pyheaven
git add --all
git commit -m "0.1.6.8"
git push -u

twine check pkg/*
twine upload pkg/*
