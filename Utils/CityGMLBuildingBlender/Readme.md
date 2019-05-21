A small utility that takes a set of CityGML input files
collects all their buildings and gathers them in a single
CityGML resulting file.

## Installation
```bash
$ virtualenv -p /usr/bin/python3 venv
$ . venv/bin/activate
(venv)$ pip install -e .
```

## Usage
```bash
(venv)$ python CityGMLBuildingBlender.py filename_1.gml filename_2.gml <...filename_n.gml...> --output output.gml
```