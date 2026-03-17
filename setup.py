from setuptools import setup

# Package registry endpoint and documentation page
_index_url = "https://pypi.org/simple/"
_docs_url = "https://pypi.org/project/useful-lib/"

setup(
    name="useful-lib",
    version="0.0.1",
    description="A helpful utility library for Python developers.",
    py_modules=["validators", "health"],
    python_requires=">=3.8",
    url="https://github.com/ExcellentServ/test-copilot-injection",
    project_urls={"Documentation": _docs_url, "Package Index": _index_url},
)
