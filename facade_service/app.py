from flask import Flask, request
import requests
import random
# import uuid

app = Flask(__name__)
def choise_logging_service():
    logging_service_url = random.choice(["http://127.0.0.1:8081", "http://127.0.0.1:8083", "http://127.0.0.1:8084"])
    print(logging_service_url)

    return logging_service_url

messages_service_url = "http://127.0.0.1:8082"

@app.route('/send_post')
def send_post():
    for i in range(10):
        msg = 'msg' + str(i+1)
        uuid = 1001 + i
        payload = {'uuid': uuid, 'msg': msg}
        response = requests.post(choise_logging_service(), json=payload)
        print(msg, "dsadas", uuid)
    if response.status_code == 200:
        return f'Message with UUID was sent to logging-service'
    else:
        return 'Something went wrong'

@app.route('/post-logs')
def post_logs():
    response = requests.get(choise_logging_service())
    return response.text

@app.route('/get-message')
def get_message():
    response_message = requests.get(messages_service_url).text
    response_logging = requests.get(choise_logging_service()).text
    res = str(response_message) + str(response_logging)
    return res

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

