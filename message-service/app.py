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
        distributed_map = client.get_map('distr_map')
        messages = distributed_map.values().result()
        print('\n --- get request from facade --- \n')
        return ','.join([msg for msg in messages]) or ''
    # return app.response_class(status=200)

def get_key_value(c, name):
    return c.kv.get(name)[1]['Value'].decode()[1:-1]


if __name__ == '__main__':
    # service_id = int(sys.argv[0])
    service_id = 1
    port = 8890
    consul_client = consul.Consul(host="consul-server")

    app.run(host="0.0.0.0",
            port=port,
            debug=False)

    client = hazelcast.HazelcastClient(
        cluster_members=get_key_value(consul_client, "hazelcast_addrs").split(',')
    )

    check_http = consul.Check.http(f'http://logging_service:{port}/', interval='10s')
    consul_client.agent.service.register(
        'logging_service',
        service_id=f'logging_service',
        address=f"logging_service",
        port=port,
        check=check_http,)
