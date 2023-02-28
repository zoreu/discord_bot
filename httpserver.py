from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def hello():
    return "Tudo online"

def run():
    app.run(host='0.0.0.0', port=80)


thread = threading.Thread(target=run)
thread.start()