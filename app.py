from flask import Flask, render_template, request, send_file
from pptx import Presentation
import time

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
    time.sleep(5)
    return render_template('download.html')

# Sending powerpoints to download
@app.route('/return-file')
def return_file():
    return send_file('users/{}.pptx'.format(topic), as_attachment=True,attachment_filename='{}.pptx'.format(topic), cache_timeout=0)

# Preventing flask from showing old cached pages
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Running the program
if __name__ == ('__main__'):
    app.run(debug=True)
