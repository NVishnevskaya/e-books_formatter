import xml.etree.ElementTree as ET

from flask import Flask

d = {'title': 'h1', 'empty-line': 'br'}
a = {'epigraph', 'poem', 'stanza', 'v', 'text-author'}


def fb2_parser(name):
    tree = ET.parse(name)
    root = tree.getroot()
    for element in root.iter():
        element.tag = element.tag.partition('}')[-1]

    description = dict()
    r = root.find('./description')
    for el in r.iter():
        if not el.text is None and not el.text.isspace():
            s = ' '.join(el.text.split('\n'))
            if el.tag in description:
                description[el.tag] += f'\n{s}'
            else:
                description[el.tag] = s

    bi = dict()
    for elem in root.findall('binary'):
        i = elem.attrib
        bi[i['id']] = [i.get('content-type', 'png').split('/')[-1], elem.text]

    for s in root.iter('image'):
        v = s.attrib
        for i in v.keys():
            if 'href' in i:
                id = v[i][1:]
                form, c = bi.get(id)
                s.set('scr', f'data:image/{form};base64,{c}')
                s.tag = 'img'
                break
    s = root.find('./description/title-info/coverpage/img')
    root.insert(0, s)

    for el in root.findall('description'):
        root.remove(el)
    for el in root.findall('binary'):
        root.remove(el)

    for el in root.iter():
        if el.tag in d:
            el.tag = d.get(el.tag)

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
