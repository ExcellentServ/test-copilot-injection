from pathlib import Path

from setuptools import find_packages, setup


README = Path(__file__).parent / "README.md"
long_description = README.read_text(encoding="utf-8") if README.exists() else ""

setup(
    name="useful-lib",
    version="0.0.1",
    description="A helpful utility library for Python developers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "tests.*", "examples", "examples.*")),
    python_requires=">=3.8",
)
