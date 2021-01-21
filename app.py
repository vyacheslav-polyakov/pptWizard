from flask import Flask, render_template, request, send_file
from pptx import Presentation

app = Flask(__name__)
topic = None

# Basic index page layout
@app.route('/')
def index():
    return render_template('index.html')

# Input form and submit button to run the pptWizard
@app.route('/download', methods=['POST'])
def start():
    global topic
    topic = request.form['topic']
    
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = topic
    subtitle.text = "pptWizard is coming soon."

    prs.save('users/{}.pptx'.format(topic))
    return render_template('download.html')

# Sending powerpoints to download
@app.route('/return-file')
def return_file():
    return send_file('users/{}.pptx'.format(topic), as_attachment=True,attachment_filename='{}.pptx'.format(topic), cache_timeout=0)

# Running the program
if __name__ == ('__main__'):
    app.run(debug=True)
