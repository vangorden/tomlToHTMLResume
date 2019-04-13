# tomlToHTMLResume
Takes resume data in a toml file, and builds a html resume based on jinja2 templates.

Project is in development, and you'll likely run into bugs.
Currently, it has only been tested on Ubuntu using python 3.7.

## Usage:
Create yourself a virtual environment using python 3.5+

Install requirements: `pip install -r requirements.txt`

Build project to content directory within project: `python toml_to_html.py`

Durring development you can optionally serve the project using the "serve" argument, which will
live reload in your browser upon saved file changes: `python toml_to_html.py server`

The `toml.resume` file should contain the data you want added to your html resume.

Your jinja2 template and associated static content should be placed in the `themes/` directory under
a directory heading that is the name of the theme. The theme should then be set in `resume.toml`
prior to building.

See the example theme in the themes directory and the resume.toml file for an example of how to 
contruct your files.
