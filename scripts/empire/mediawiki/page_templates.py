import re
from os.path import join, dirname
from pprint import pprint

from mako.template import Template

def render_page_template(lang, file, render_data):
    template = Template(filename=join(dirname(__file__), 'page_templates', lang, file))

    rendered = template.render(**render_data).strip()
    rendered_lines = rendered.splitlines()

    page_name_match = re.compile(r'= (.+) =').search(rendered_lines[0])
    if not page_name_match:
        raise Exception(f'Mediawiki page template {lang}/{file} is missing first line with the page name, eg. = Page name =')

    name = page_name_match.group(1)
    content = '\n'.join(rendered_lines[1:]).strip()

    return {
        'name': name,
        'content': content
    }
