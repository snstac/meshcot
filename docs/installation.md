MeshCOT's functionality provided by a command-line program called `meshcot`.

There are several methods of installing MeshCOT. They are listed below, in order of complexity.

## Debian, Ubuntu, Raspberry Pi

Install MeshCOT, and prerequisite packages of [PyTAK](https://pytak.rtfd.io).

```sh linenums="1"
sudo apt update
wget https://github.com/ampledata/pytak/releases/latest/download/python3-pytak_latest_all.deb
sudo apt install -f ./python3-pytak_latest_all.deb
wget https://github.com/ampledata/meshcot/releases/latest/download/python3-meshcot_latest_all.deb
sudo apt install -f ./python3-meshcot_latest_all.deb
```

## Windows, Linux

Install from the Python Package Index (PyPI) [Advanced Users]::

```sh
sudo python3 -m pip install meshcot
```

## Developers

PRs welcome!

```sh linenums="1"
git clone https://github.com/snstac/meshcot.git
cd meshcot/
python3 setup.py install
```
