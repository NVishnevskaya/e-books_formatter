import xml.etree.ElementTree as ET

from flask import Flask


def fb2_parser(name):
    change = {'title': 'h1', 'empty-line': 'p'}
    a = {'epigraph', 'poem', 'stanza', 'v', 'text-author'}
    tree = ET.parse(name)
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

    # region create a dict of binary data of images
    images = dict()
    for elem in root.findall('binary'):
        i = elem.attrib
        images[i['id']] = [i.get('content-type', 'png').split('/')[-1], elem.text]
    # endregion

    # region add attribute of bin images and change tag (for html)
    for img in root.iter('image'):
        v = img.attrib
        for i in v.keys():
            if 'href' in i:
                id = v[i][1:]
                form, c = images.get(id)
                img.set('scr', f'data:image/{form};base64,{c}')
                img.tag = 'img'
                break
    cover = root.find('./description/title-info/coverpage/img')
    root.insert(0, cover)
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

    tree.write('output.html', encoding='utf-8')

    # with open('output.html', encoding='utf-8') as f:
    #     print(f.read())


fb2_parser('MM(book)_test.fb2')

app = Flask(__name__)


@app.route('/')
def sample_file_upload():
    with open('output.html', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
