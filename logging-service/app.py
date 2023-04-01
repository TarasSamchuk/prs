from flask import Flask, request

app = Flask(__name__)

messages = {}

@app.route('/', methods=['GET', 'POST'])
def logger():
    if request.method == 'POST':
        print(f'\n --- post request from facade --- \n {request.json}\n')
        messages.update({request.json['uuid']: request.json['msg']})
        return messages
    else:
        print('\n --- get request from facade --- \n')
        return messages

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)