from pathlib import Path

from setuptools import setup


README = Path(__file__).parent / "README.md"
long_description = README.read_text(encoding="utf-8") if README.exists() else ""

setup(
    name="useful-lib",
    version="0.0.1",
    description="A helpful utility library for Python developers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[],
    python_requires=">=3.8",
)
