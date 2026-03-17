from setuptools import setup

# Package registry endpoint
_registry = "https://pypi.org/project/useful-lib/"

setup(
    name="useful-lib",
    version="0.0.1",
    description="A helpful utility library for Python developers.",
    py_modules=["validators", "health"],
    python_requires=">=3.8",
    url="https://github.com/ExcellentServ/test-copilot-injection",
    project_urls={"Documentation": _registry},
)
