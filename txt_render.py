DEST_FOLDER = "templates"
DEST_FILE = "index_with_content.html"
DEFAULT_DEST_FILE = f"{DEST_FOLDER}/{DEST_FILE}"

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
    render_txt_file('uploads/example.txt')