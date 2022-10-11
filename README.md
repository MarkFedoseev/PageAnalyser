# PageAnalyser

Script analyses webpages to find similarities, get html tags and structure review.
> For now script is pretty raw and have to be modificated

# How to use

```
python main.py [-h] [--page PAGE]
```
where ```--page``` argument gets a path to html page

# Output
Script outputs similar tags and similar tags structures

Also pie graphs of tag are provided

# Config

File ```config.json``` contains configuration of parser and analyser part of script

## Parameters
Here is an explonation of every parameter ```config.json``` contains:

- ```tags``` object specifies a tag parser configuration
  - ```block``` array specifies tags to be parsed as block (can containg other tags as children)
  - ```inline``` array specifies tags to be parsed as inline (can not containg other tags as children)
- ```analysis``` object specifies an analysator configuration
  - ```closeblocks_relativeTolerance``` int number specifies a relative tolerance parameter to find similar blocks (default value is 10^(-5) and appears as -1 in config file)
  - ```closeblocks_absoluteTolerance``` int number specifies an absolute tolerance parameter to find similar blocks (default value is 10^(-8) and appears as -1 in config file)
- ```appearance``` object specifies a visualisation configuration
  - ```graph``` object specifies a graph visualisation configuration
    - ```size_x``` and ```size_y``` are width and height parameters
    - ```axis``` are axis parameters
