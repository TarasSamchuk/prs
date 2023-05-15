from flask import Flask, request
import requests
import random
import hazelcast
# import uuid

app = Flask(__name__)
def choise_logging_service():
    logging_service_url = random.choice(["http://127.0.0.1:8081", "http://127.0.0.1:8083", "http://127.0.0.1:8084"])
    print(logging_service_url)
    return logging_service_url

def choise_message_service():
    messages_service_url = random.choice(["http://127.0.0.1:8082", "http://127.0.0.1:8086"])
    return messages_service_url

@app.route('/send_post')
def send_post():
    for i in range(10):
        msg = 'msg' + str(i+1)
        uuid = 1001 + i
        payload = {'uuid': uuid, 'msg': msg}
        response = requests.post(choise_logging_service(), json=payload)
        print(payload)
        queue.put(payload)

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
    response_message = requests.get(choise_message_service()).text
    response_logging = requests.get(choise_logging_service()).text
    res = "Response message: " + str(response_message) + "\n" + "Response logging: " + str(response_logging)
    return res

# @app.route("/facade_service", methods=['GET'])
# def facade_get():
#     logging_service = requests.get(url=random.choice(logging_services_url))
#     messages_service = requests.get(random.choice(messages_services_addresses))
#     return_string = "logging_service:" + logging_service.text + "\n messages_service: " + messages_service.text
#     return return_string


if __name__ == '__main__':
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue")
    app.run(host='127.0.0.1', port=8085)

