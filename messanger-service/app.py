from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_message():
    return 'NOT IMPLEMENTED YET'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082)