import re
from os.path import join, dirname
from pprint import pprint

from mako.template import Template

def render_page_template(lang, file, render_data):
    template = Template(filename=join(dirname(__file__), 'page_templates', lang, file))

    def format_amount(num):
        if not num:
            return ''

        formatted = "{:,.2f}".format(num)

        if lang == 'cs':
            formatted = formatted.replace(',', ' ').replace('.', ',')

        return formatted

    render_data['to_s'] = lambda v: v if v is not None else ''
    render_data['format_amount'] = format_amount

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


def prepare_template(lang, file):
    return Template(filename=join(dirname(__file__), 'page_templates', lang, file))


def to_s(v):
    return v if v is not None else ''


def render_prepared_template(lang, file, template, render_data):
    def format_amount(num):
        if not num:
            return ''

        formatted = "{:,.2f}".format(num)

        if lang == 'cs':
            formatted = formatted.replace(',', ' ').replace('.', ',')

        return formatted

    render_data['to_s'] = to_s
    render_data['format_amount'] = format_amount

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
