from flask import Flask, send_file, request
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from pptx import Presentation

app = Flask(__name__)

# Basic index page layout
@app.route('/')
def index():
    return '<body>\
                <a href=/generate-file/>\
                        <button class="btn btn-default">\
                            Generate Powerpoint\
                        </button>\
                    </a>\
                    <a href=/return-file/ target=_blank>\
                        <button class="btn btn-default">\
                            Download\
                        </button>\
                    </a>\
                    \
                    <form method="POST">\
                        <input type="text" name="topic" maxlength="100"/>\
                        <input name="submit" />\
                    <form>\
                    \
                </body>'

'''
# Creating forms from within flask to be rendered in html
class TopicForm(Form):
    topic = StringField('Topic:', validators=[Required()])
    submit = SubmitField('Submit')
'''
# A simpler way to process topic input?
@app.route('/', methods=['POST'])
def process_topic():
    topic = request.form['text']
    return 'Your topic is ', topic

# Generating powerpoints
@app.route('/generate-file/')
def generate_file():
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = 'Hello, World!'
    subtitle.text = "pptWizard is coming soon."

    prs.save('users/hello.pptx')
    return 'Hello, World!'

# Sending powerpoints to download
@app.route('/return-file/')
def return_file():
    return send_file('users/hello.pptx', as_attachment=True,attachment_filename='hello.pptx', cache_timeout=0)

# Running the program
if __name__ == ('__main__'):
    app.run(debug=True)
