from ebooklib import epub
from bs4 import BeautifulSoup
import ebooklib
from renders.level_up import get_default_t_file

tag_exception = ['body', 'head']
DEFAULT_DEST_FILE = get_default_t_file()


def get_epub_item_doc(filename):
    book = epub.read_epub(filename)
    items_doc = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            item_content = item.get_content().decode()
            soup = BeautifulSoup(item_content, 'html.parser')
            item_content = soup.prettify()
            items_doc.append(item_content)
    return items_doc


def get_epub_style(filename):
    book = epub.read_epub(filename)
    items_styles = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_STYLE:
            item_content = item.get_content().decode()
            soup = BeautifulSoup(item_content, 'html.parser')
            item_content = soup.prettify()
            items_styles.append(item_content)
    resp = "\n".join(items_styles)
    return resp


def set_epub_style(filename, dest_file=DEFAULT_DEST_FILE):
    file_content = get_epub_style(filename)
    with open(dest_file, mode="a", encoding="UTF-8") as file:
        file.write('<style>\n')
        file.write(file_content + '\n')
        file.write('</style>\n')


def get_epub_style_text(filename):
    file_content = get_epub_style(filename)
    answer = [
        '<style>\n',
        file_content,
        '</style>\n'
    ]
    answer = "\n".join(answer)
    return answer


def render_epub_to_html(filename, dest_file=DEFAULT_DEST_FILE):
    file_content = get_epub_item_doc(filename)[0]
    with open(dest_file, mode="w", encoding="UTF-8") as file:
        file.write('{% extends "base_index.html" %}\n')
        file.write('{% block content %}\n')
        file.write(file_content + '\n')
        file.write(get_epub_style_text(filename))
        file.write('{% endblock %}\n')


if __name__ == "__main__":
    render_epub_to_html('files_set/test.epub')
