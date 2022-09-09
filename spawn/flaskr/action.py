from flask import Flask

app = Flask(__name__)


@app.route('/api/v1/system/<string:system>/actors/<string:name>/invoke', methods=["POST"])
def action(name: str, system: str):
    return 'Hello, World!'
