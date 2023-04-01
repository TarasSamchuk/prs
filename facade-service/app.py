from flask import Flask, request
import requests
# import uuid

app = Flask(__name__)

logging_service_url = "http://127.0.0.1:8081"
messages_service_url = "http://127.0.0.1:8082"

@app.route('/send_post')
def send_post():
    msg = 'msg'
    uuid = 1001
    payload = {'uuid': uuid, 'msg': msg}
    response = requests.post(logging_service_url, json=payload)
    if response.status_code == 200:
        return f'Message with UUID was sent to logging-service'
    else:
        return 'Something went wrong'

@app.route('/post-logs')
def post_logs():
    response = requests.get(logging_service_url)
    return response.text

@app.route('/get-message')
def get_message():
    response_message = requests.get(messages_service_url).text
    response_logging = requests.get(logging_service_url).text
    res = str(response_message) + str(response_logging)
    return res

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

