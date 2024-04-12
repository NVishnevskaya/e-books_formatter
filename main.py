# flask import
from flask import Flask, render_template, request, redirect, url_for
import os
# database import
from data import db_session
from data.users import User
# renders' import
import epub_render
import txt_render
import style_render
# raters and generators
import placeholder_generator as pg
from password_rate import is_correct_password
# flask-wtf import
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    is_reg = BooleanField('Регистрация')
    submit = SubmitField('Войти')

    def validate_on_submit(self):
        if '@' not in str(self.email):
            return False
        return True


db_session.global_init("db/data.db")
ALLOWED_EXTENSIONS = {'epub', 'fb2', 'pdf', 'txt'}
app = Flask(__name__, template_folder="templates")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

UPLOAD_FOLDER = 'uploads'
DESTINATION_FILE_FOR_CONTENT = 'index_with_content.html'
DEFAULT_FOLDER = "templates"
DEFAULT_FILE_WITH_CONTENT = f"{DEFAULT_FOLDER}/{DESTINATION_FILE_FOR_CONTENT}"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


current_settings = {
    "is_file_loaded": False,
    "font-size": 16,
    "font-family": "",
    "author_of_the_day_quote": "",
    "the_day_quote": "",
    "fonts": {
        "arial": ['selected', "Arial, Helvetica, sans-serif"],
        "comic_sans": ['', '"Comic Sans MS", "Comic Sans", cursive'],
        '-': ['', None]
    },
    "font-colors": {
        "black": 'selected',
        "brown": '',
    },
    "auth_info": {
        'is_reg': 'none',

    }
}


def set_new_quote():
    resp_quote = pg.get_quote_of_the_day()
    current_settings["author_of_the_day_quote"], current_settings["the_day_quote"] = resp_quote['author'], resp_quote[
        'quote']


def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def change_style(filename=DEFAULT_FILE_WITH_CONTENT):
    content_lines = []
    with open(filename, mode="a", encoding="UTF-8") as file:
        content_lines = file.readlines()


def allowed_file(filename):
    return '.' in filename and get_file_extension(filename) in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def show_main_page():
    set_new_quote()
    if current_settings['is_file_loaded']:
        return render_template(DESTINATION_FILE_FOR_CONTENT, font_size=f'{current_settings["font-size"]}',
                               day_quote=current_settings['the_day_quote'],
                               author_quote=current_settings["author_of_the_day_quote"],
                               arial_state=current_settings["fonts"]["arial"][0],
                               comic_sans_state=current_settings["fonts"]["comic_sans"][0],
                               no_state=current_settings["fonts"]["-"][0],
                               black_state=current_settings["font-colors"]["black"],
                               brown_state=current_settings["font-colors"]["brown"]
                               )
    return render_template('index.html', text="", font_size=f'{current_settings["font-size"]}',
                           day_quote=current_settings['the_day_quote'],
                           author_quote=current_settings["author_of_the_day_quote"],
                           arial_state=current_settings["fonts"]["arial"][0],
                           comic_sans_state=current_settings["fonts"]["comic_sans"][0],
                           no_state=current_settings["fonts"]["-"][0],
                           black_state=current_settings["font-colors"]["black"],
                           brown_state=current_settings["font-colors"]["brown"]
                           )


@app.route('/new_style', methods=["POST", "GET"])
def set_new_style():
    if request.method == "POST":
        # font size
        cur_font_size = request.form.get('font-size')
        current_settings['font-size'] = cur_font_size
        # font family
        cur_font_family = request.form.get('font-family')
        for key in current_settings['fonts'].keys():
            current_settings['fonts'][key][0] = ''
        current_settings['fonts'][cur_font_family][0] = 'selected'
        # font color
        cur_font_color = request.form.get('text-color')
        for key in current_settings['font-colors'].keys():
            current_settings['font-colors'][cur_font_color] = ''
        current_settings['font-colors'][cur_font_color] = 'selected'
        # style render
        style_render.render_css(new_font_size=cur_font_size, new_font_color=cur_font_color,
                                new_font_family=current_settings['fonts'][cur_font_family][1])
    return redirect(url_for('show_main_page'))


@app.route('/reset_file', methods=["GET", "POST"])
def clear_temp_file():
    current_settings['is_file_loaded'] = False
    return redirect(url_for('show_main_page'))


@app.route('/return_file', methods=["GET", "POST"])
def return_temp_file():
    current_settings['is_file_loaded'] = True
    return redirect(url_for('show_main_page'))


@app.route('/refer_to_auth', methods=["GET", "POST"])
def show_auth_page():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('show_main_page'))
    return render_template('auth_page.html', form=form)


@app.route('/refer_to_auth/to_main_page', methods=["GET", "POST"])
def return_to_main_page_from_auth():
    return redirect(url_for('show_main_page'))


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
            current_settings['is_file_loaded'] = True
            if ext == "epub":
                epub_render.render_epub_to_html(file_path)
            elif ext == "txt":
                txt_render.render_txt_file(file_path)
        return redirect(url_for('show_main_page'))


if __name__ == '__main__':
    app.run()
