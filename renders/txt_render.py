from renders.level_up import get_default_t_file

DEFAULT_DEST_FILE = get_default_t_file()

def get_txt_text(filename):
    with open(filename, mode="r", encoding="UTF-8") as file:
        text = file.readlines()
    text = list(map(lambda x: f"<p>{x.strip()}</p>", text))
    text.append("\n<style>")
    text.append("</style>\n")
    return "\n".join(text)


def render_txt_file(filename, dest_file=DEFAULT_DEST_FILE):
    resp = get_txt_text(filename)
    with open(dest_file, mode="w", encoding="UTF-8") as file:
        file.write('{% extends "base_index.html" %}\n')
        file.write('{% block content %}\n')
        file.write(resp)
        file.write('{% endblock %}\n')

if __name__ == "__main__":
    print(DEFAULT_DEST_FILE)