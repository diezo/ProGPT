from distutils.core import setup
from pathlib import Path

version = "1.0.2"
long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="ProGPT",
    packages=["ProGPT"],
    version=version,
    license="MIT",
    description="❄️ Python Package To Access GPT-3.5 Free Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Deepak Soni",
    author_email="sonniiii@outlook.com",
    url="https://github.com/diezo/progpt",
    download_url=f"https://github.com/diezo/progpt/archive/refs/tags/v{version}.tar.gz",
    keywords=[
        "progpt",
        "chatgpt",
        "gpt-3.5",
        "python-gpt",
        "python-chatgpt",
        "ai",
        "generative-ai",
        "chatgpt-ai",
        "python-ai",
        "python-generative-ai"
    ],
    install_requires=[
        "requests",
        "selenium"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10"
    ]
)
