from bs4 import BeautifulSoup
from renders.level_up import get_default_t_file

DEFAULT_FILE_WITH_CONTENT = get_default_t_file()


def get_style_block(filename=DEFAULT_FILE_WITH_CONTENT):
    with open(filename, encoding="UTF-8", mode="r") as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    try:
        content = soup.find('style').text
        return content
    except AttributeError:
        return ''


def reformat_css_to_dict(text, remove_empty_lines=False):
    css_list = text.split("\n")
    css_lines = list(map(lambda x: x.strip(), css_list))
    data_dict = dict()
    start_index = 0
    new_key = ''
    for index in range(len(css_lines)):
        if '{' in css_lines[index]:
            new_key = css_lines[index].replace('{', '').strip()
            data_dict[new_key] = []
            start_index = index + 1
        if '}' in css_lines[index]:
            data_dict[new_key] = css_lines[start_index:index]
            if remove_empty_lines:
                data_dict[new_key] = list(filter(lambda x: x.strip() != '', data_dict[new_key]))
    return data_dict


def insert_tag_to_css(css_dict, enclosure=False, font_size=16, font_color="black", font_family=None):
    if enclosure:
        pass
    else:
        if 'p' in css_dict.keys():
            needed_indexes = list(
                filter(lambda x: ('font-size' in css_dict['p'][x]) or (css_dict['p'][x].startswith('color:')),
                       [index for index in range(len(css_dict['p']))]))
            if font_family is not None:
                additional_indexes = list(filter(lambda x: 'font-family' in css_dict['p'][x],
                                                 [index for index in range(len(css_dict['p']))]))
                needed_indexes += additional_indexes
            for index in needed_indexes:
                css_dict['p'][index] = ""
            css_dict['p'].append(f'font-size: {font_size}px;')
            css_dict['p'].append(f'color: {font_color};')
            if font_family is not None:
                css_dict['p'].append(f'font-family: {font_family};')
        else:
            css_dict['p'] = []
            css_dict['p'].append(f'font-size: {font_size}px;')
            css_dict['p'].append(f'color: {font_color};')
            css_dict['p'].append(f'font-family: {font_family};')
        css_dict['p'] = list(filter(lambda x: x.strip() != "", css_dict['p']))
    return css_dict


def reformat_dict_to_css(css_dict):
    answer = list()
    answer.append('<style>')
    for key, value in css_dict.items():
        new_key = key + ' {'
        processed_data = list(map(lambda x: f'\t{x}', value))
        new_content = "\n".join(processed_data)
        answer.append(new_key)
        answer.append(new_content)
        answer.append('}\n')
    answer.append('</style>')
    return '\n'.join(answer)


def remove_previous_file(html_list):
    block_lines = tuple(
        filter(lambda index: html_list[index].strip() == "{% endblock %}", [index for index in range(len(html_list))]))
    endblock_index = block_lines[0]
    html_list = html_list[:endblock_index] + html_list[endblock_index + 1:]
    suitable_indexes = tuple(
        filter(lambda index: html_list[index].strip() == "<style>" or html_list[index].strip() == "</style>",
               [index for index in range(len(html_list))]))
    start_index, end_index = suitable_indexes[0], suitable_indexes[-1]
    new_data = html_list[:start_index] + html_list[end_index + 1:]
    return new_data


def insert_to_html_file(content, filename=DEFAULT_FILE_WITH_CONTENT):
    with open(filename, mode="r", encoding="UTF-8") as html_file:
        html_lines = html_file.readlines()
    html_lines = remove_previous_file(html_lines)
    html_content = ''.join(html_lines)
    new_content = f"{html_content}\n{content}\n{'{% endblock %}'}"
    with open(filename, mode="w", encoding="UTF-8") as html_file:
        html_file.write(new_content)


def render_css(filename=DEFAULT_FILE_WITH_CONTENT, new_font_size=16, new_font_color='black', new_font_family=None):
    css_data = get_style_block(filename)
    formatted_dict = reformat_css_to_dict(css_data, remove_empty_lines=True)
    formatted_dict = insert_tag_to_css(formatted_dict, font_size=new_font_size, font_color=new_font_color,
                                       font_family=new_font_family)
    new_css = reformat_dict_to_css(formatted_dict)
    insert_to_html_file(new_css)


if __name__ == "__main__":
    render_css()
