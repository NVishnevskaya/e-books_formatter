from flask import Flask, render_template
import PyPDF2


app = Flask(__name__, template_folder="templates")


@app.route('/')
def show_start_page():
    pdf_file = open('files_set/book1.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_list = pdf_reader.pages[34].extract_text()
    pdf_file.close()
    return render_template('start_page.html', text=text_list)


if __name__ == "__main__":
    app.run()
