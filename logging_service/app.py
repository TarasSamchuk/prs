from flask import Flask, request
import hazelcast

app = Flask(__name__)

messages = {}

@app.route('/', methods=['GET', 'POST'])
def logger():
    if request.method == 'POST':
        print(f'\n --- post request from facade --- \n {request.json}\n')
        distributed_map = client.get_map('distr_map')
        distributed_map.set(str(request.json['uuid']), str(request.json['msg']))
        print('--- SUCCESSFULLY SAVED ---')
        return app.response_class(status=200)
    else:
        distributed_map = client.get_map('distr_map')
        messages = distributed_map.values().result()
        print('\n --- get request from facade --- \n')
        return ','.join([msg for msg in messages]) or ''

if __name__ == '__main__':
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5701"]
    )
    app.run(host='127.0.0.1', port=8081)
