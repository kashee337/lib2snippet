from setuptools import find_packages, setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="lib2snippet",
    packages=find_packages(),
    install_requires=_requires_from_file("requirements.txt"),
    url="https://github.com/kashee337/lib2snippet.git",
    version="0.1.0",
    description="register for vscode snippet",
    author="kashee337",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "tosnip = lib2snippet:main",
        ],
    },
)
