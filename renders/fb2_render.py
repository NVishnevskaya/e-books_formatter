import xml.etree.ElementTree as ET
from renders.level_up import get_default_t_file

DEFAULT_DEST_FILE = get_default_t_file()


def render_fb2_file(filename, dest_filename=DEFAULT_DEST_FILE):
    change = {'title': 'h1', 'empty-line': 'p'}
    a = {'epigraph', 'poem', 'stanza', 'v', 'text-author'}
    tree = ET.parse(filename)
    root = tree.getroot()
    for element in root.iter():
        element.tag = element.tag.partition('}')[-1]

    # region create a dict of metadata
    description = dict()
    r = root.find('./description')
    for el in r.iter():
        if not (el.text is None) and not el.text.isspace():
            text = ' '.join(el.text.split('\n'))
            if el.tag in description:
                description[el.tag] += f'\n{text}'
            else:
                description[el.tag] = text
    # endregion

    # region remove unused tags
    for el in root.findall('description'):
        root.remove(el)
    for el in root.findall('binary'):
        root.remove(el)
    # endregion

    # region change tags for html 
    for el in root.iter():
        if el.tag in change:
            el.tag = change.get(el.tag)
    # endregion

    with open(dest_filename, mode="wb") as file:
        file.write('{% extends "base_index.html" %}\n'.encode('utf-8'))
        file.write('{% block content %}\n'.encode('utf-8'))
        tree.write(file)
        file.write('<style>\n</style>\n'.encode('utf-8'))
        file.write('{% endblock %}\n'.encode('utf-8'))


