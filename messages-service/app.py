import threading
from flask import Flask, request
import hazelcast

app = Flask(__name__)

@app.route("/", methods=['GET'])
def messages_get():
    return_messages = str(list(dict.values()))
    print(return_messages)
    return return_messages


def def_thread():
    while True:
        if not queue.is_empty():
            head = queue.take()
            dict.update({str(head['uuid']): head['msg']})
            print(dict)


if __name__ == '__main__':
    dict = {}
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5701"]
    )
    queue = client.get_queue("queue").blocking()
    consumer_thread = threading.Thread(target=def_thread)
    consumer_thread.start()

    app.run(host='127.0.0.1', port=8082, debug=False)
