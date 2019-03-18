"""
Command line utility to build a html resume from a passed jinja2 template
and a toml file with resume data. Alpha quality, use at your own risk! Running
script will build index.html and associated in content directory. Script
accepts an optional "serve" argument, which will serve the content directory
over http, at http://127.0.0.1:5500

Usage: pip3 install requirements.txt
       python3 toml_to_html.py serve
"""

import pathlib
import shutil
import sys

import toml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

resume_dict = {}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()
    else:
        build()


def serve():
    '''Serves the resume over http using livereload utility
       Assumes: resume.toml file is in project root, and there is a theme
       directory that contains a directory with the name of the theme
       specified in resume.toml.
    '''
    resume_dict = build()
    server = Server()
    server.watch("resume.toml", build)
    server.watch('themes/'+resume_dict["theme"], build)
    if pathlib.Path('themes/'+resume_dict["theme"]+'/static').is_dir():
        server.watch('themes/'+resume_dict["theme"]+'/static/*', build)
    server.serve(root='content/')


def build():
    ''' Parses toml file and theme template to build index.html and place
    it and its associated static content to content directory.
    '''
    # ensure content dir exists to write output
    pathlib.Path('content').mkdir(parents=True, exist_ok=True)

    resume_dict = toml.load('resume.toml')

    # check for static dir in theme, and copy over to content
    if pathlib.Path('themes/'+resume_dict["theme"]+'/static').is_dir():
        if pathlib.Path('content/static').is_dir():
            shutil.rmtree('content/static')
        shutil.copytree(
            'themes/'+resume_dict["theme"]+"/static", 'content/static')

    env = Environment(
        loader=FileSystemLoader('themes/'+resume_dict["theme"]),
        autoescape=select_autoescape(['html', 'xml']))

    template = env.get_template(resume_dict["theme"] + ".html")
    render = template.render(data=resume_dict)
    with open("content/index.html", "w") as f:
        f.write(render)

    return resume_dict


main()
