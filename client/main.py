import asyncio
import logging

from client4game1 import zeebe_client
from flask import Flask, abort, jsonify
from flask import request
from gevent.pywsgi import WSGIServer

loop = asyncio.get_event_loop()
app = Flask(__name__)

logger = logging.getLogger(__file__)
logger.info("APP STARTED")


async def zeebe_run(task):
    print(task)
    # Run a Zeebe process instance
    process_instance_key = await zeebe_client.run_process(bpmn_process_id="Process_game", variables=task)
    print(process_instance_key)


@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'weapon' in request.json:
        abort(400)

    loop.run_until_complete(zeebe_run(request.json))

    return jsonify({'task': request.json}), 201


async def main():
    # Deploy a BPMN process definition
    await zeebe_client.deploy_process("process.bpmn")
    print('deployed')


if __name__ == '__main__':
    loop.run_until_complete(main())
    # app.run(host="0.0.0.0", port=8080)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

# # Cancel a running process
# await zeebe_client.cancel_process_instance(process_instance_key=12345)
#
# # Publish message
# await zeebe_client.publish_message(name="message_name", correlation_key="some_id")
