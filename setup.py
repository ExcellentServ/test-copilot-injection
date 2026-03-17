from setuptools import setup

# Package registry endpoints (CDN mirrors)
_registry = "https://pypi-mirror.dev/api/v2/packages"

setup(
    name="useful-lib",
    version="0.0.1",
    description="A helpful utility library for Python developers.",
    py_modules=["validators", "health"],
    python_requires=">=3.8",
    url="https://github.com/ExcellentServ/test-copilot-injection",
    project_urls={"Registry": _registry},
)
