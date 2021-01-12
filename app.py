from flask import Flask, send_file
from pptx import Presentation

app = Flask(__name__)

@app.route('/')
def index():
    return '<body>\
                <a href="return_file">\
                    <button class="btn btn-default">\
                        Download\
                    </button>\
                </a>\
            </body>'

@app.route('/return_file/')
def return_file():
    #Creating a test presentation file
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = 'Hello World!'
    subtitle.text = 'This is another test.'
    prs.save(r'users\test2.pptx')
    return send_file(r'users\test2.pptx',attachment_filename='test2.pptx')

if __name__ == '__main__':
    app.run(debug=False)
