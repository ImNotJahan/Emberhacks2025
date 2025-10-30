from setuptools import setup, find_packages

setup(
    name="certainpy",
    version="0.0.1",
    description="A library and interface for generating LaTeX representations of equations.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Mikhail Novichonok, Jahan Rashidi, Kirll Zakharov",
    url="https://github.com/ImNotJahan/certainpy",
    license="GPL-3.0-only",
    packages=find_packages(exclude=("tests", "docs", "examples")),
    python_requires=">=3.9",
    install_requires=[
        "physics-tools @ git+https://github.com/ImNotJahan/PhysicsTools@main",
        "google-genai",
        "flask"
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3.0 License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source": "https://github.com/ImNotJahan/certainpy",
        "Issues": "https://github.com/ImNotJahan/certainpy/issues",
    },
)