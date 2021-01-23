from flask import Flask, render_template

app = Flask(__name__, static_folder='../frontend/greenship/build/static', template_folder='../frontend/greenship/build')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scrape/<tracking>/', methods=["POST", "GET"])  # GET is only there as a test
def scrape(tracking):
    return "scraping {}...".format(tracking)

@app.route('/info/<tracking>/', methods=["GET"])
def getInfo(tracking):
    return "getting {} info...".format(tracking)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
