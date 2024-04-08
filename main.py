from flask import Flask, render_template, request, redirect, url_for
import epub_render
import txt_render
import os

ALLOWED_EXTENSIONS = {'epub', 'fb2', 'pdf', 'txt'}
app = Flask(__name__, template_folder="templates")

UPLOAD_FOLDER = 'uploads'
DESTINATION_FILE_FOR_CONTENT = 'index_with_content.html'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
current_settings = {
    "processed_file": None
}


def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename):
    return '.' in filename and get_file_extension(filename) in ALLOWED_EXTENSIONS


@app.route('/')
def show_main_page():
    return render_template('index.html', text="")

@app.route('/new_style', methods=["POST", "GET"])
def set_new_style():
    return redirect(url_for('show_index_with_content'))

@app.route('/upload', methods=['GET', 'POST'])
def handle_file_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('show_main_page'))
        uploaded_file = request.files.getlist("file")[0]
        if uploaded_file.filename.strip() == "":
            return redirect(url_for('show_main_page'))
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = uploaded_file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)
            ext = get_file_extension(file_path)
            if ext == "epub":
                epub_render.render_epub_to_html(file_path)
            elif ext == "txt":
                txt_render.render_txt_file(file_path)
            # необходимо форматировать полученный файл в html, унаследовав от base_index.html
            return redirect(url_for('show_index_with_content'))
        return redirect(url_for('show_main_page'))


@app.route('/with_content', methods=['GET', 'POST'])
def show_index_with_content():
    return render_template(DESTINATION_FILE_FOR_CONTENT)


if __name__ == '__main__':
    app.run()
