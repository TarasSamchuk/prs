from flask import Flask, request
import hazelcast
import consul
import sys

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
        # distributed_map = client.get_map('distr_map')
        # messages = distributed_map.values().result()
        print('\n --- get request from facade --- \n')
        return ','.join([msg for msg in messages]) or ''
    # return app.response_class(status=200)

def get_key_value(c, name):
    return c.kv.get(name)[1]['Value'].decode()[1:-1]


if __name__ == '__main__':
    host = "127.0.0.1"
    port = 8082
    app.run(host=host, port=port)
    consul_service = consul.Consul()
    consul_service.agent.service.register(name="logging_service",
                                          service_id="logging_service",
                                          address=host,
                                          port=port,
                                          check={"name": "Checks the logging1 http response",
                                                 f"http": "http://" + host + ":" + str(port) + "/service_check",
                                                 "interval": "10s"})

    client = hazelcast.HazelcastClient()
    index, data = consul_service.kv.get("hazelcast_map")
    haz_map_name = data["Value"].decode()[:-1].replace('"', "")
    logging_map = client.get_map(haz_map_name).blocking()
    app.run(host=host,
            port=port,
            debug=False)

