from PyPDF2 import PdfReader
from renders.level_up import get_default_t_file

DEFAULT_DEST_FILE = get_default_t_file()


def get_pdf_info(filename):
    reader = PdfReader(filename)
    quantity_of_pages = len(reader.pages)
    result = dict()
    for index in range(quantity_of_pages):
        raw_content = reader.pages[index].extract_text()
        result[index + 1] = raw_content.split('\n')
    return result


def convert_to_css(dict_content):
    new_list_content = []
    for key, value in dict_content.items():
        val_cont = "".join(tuple(map(lambda x: f'<p> {x} </p>\n', value)))
        val_cont += '<div class="create-line"></div>\n'
        val_cont += f'<div class="page_num"> {key} </div>\n'
        new_list_content.append(val_cont)
    new_list_content.append('<style>\n')
    new_list_content.append(
        """.create-line {\n\twidth: 250px;\n\tborder-top: 1px solid #493726;\n\tmargin: 5px;\n}\n""")
    new_list_content.append(""".page_num {\n\t font-size: 11px;\n\tfont-color: #616161;\n\tmargin: 3px 3px 30px;\n}\n""")
    new_list_content.append('</style>\n')
    result = ''.join(new_list_content)
    return result


def get_pdf_text(filename):
    pdf_dict = get_pdf_info(filename)
    css_content = convert_to_css(pdf_dict)
    return css_content


def render_pdf_file(filename, dest_file=DEFAULT_DEST_FILE):
    resp = get_pdf_text(filename)
    with open(dest_file, mode="w", encoding="UTF-8") as file:
        file.write('{% extends "base_index.html" %}\n')
        file.write('{% block content %}\n')
        file.write(resp)
        file.write('{% endblock %}\n')


if __name__ == "__main__":
    print(convert_to_css('input.pdf'))
