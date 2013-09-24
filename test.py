from flask import Flask
from flaskext.shorteners import GoogleShortener, BitlyShortener
app = Flask(__name__)

@app.route("/")
def hello():
    url = 'http://www.google.com'
    googl = GoogleShortener(url)
    short = GoogleShortener('http://goo.gl/fbsS')
    bitly = BitlyShortener(url, app=app)
    short_bit = BitlyShortener('http://bit.ly/1eDfN0v', app=app)
    return """
    <h1>Hello World! Testing www.google.com </h1>
    <h2>Google</h2>
    <p>{} - {}</p>
    <h2>Bit.ly</h2>
    <p>{} - {}</p>""".format(googl.short(), short.expand(), bitly.short(),
                             short_bit.expand())


if __name__ == "__main__":
    # Put the right configs otherwise it will return None
    app.config['BITLY_LOGIN'] = 'YOUR_LOGIN'
    app.config['BITLY_API_KEY'] = 'YOUR_API_KEY'
    app.run('0.0.0.0', debug=True)
