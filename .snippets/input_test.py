from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return '<html>\
                <body>\
                    <form action="/act" method="POST">\
                        <input type="text" name="sushi" maxlength="100" />\
                        <button type="submit" />\
                    </form>\
                </body>\
                </html>'

@app.route('/act', methods=['POST'])
def act():
    name = request.form['sushi']
    return 'Hello, {0}!'.format(name)



if __name__ == '__main__':
    app.run(debug=True)
