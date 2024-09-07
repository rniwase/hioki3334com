
#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages


setup(
    name                 = "hioki3334com",
    description          = "Control Hioki 3334 power meter via RS232C",
    author               = "Ryohei Niwase",
    author_email         = "rniwase@lila.cs.tsukuba.ac.jp",
    url                  = "https://github.com/rniwase",
    download_url         = "https://github.com/rniwase/hioki3334com",
    license              = "BSD",
    python_requires      = "~=3.7",
    packages             = find_packages(where=("hioki")),
    install_requires     = ["pyserial"],
)
