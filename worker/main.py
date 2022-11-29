import asyncio
import os
import random
import pika
import json

from pyzeebe import ZeebeWorker, Job, create_insecure_channel

channel = create_insecure_channel(hostname=os.environ["ZEEBE_HOST"], port=26500)  # Create grpc channel
worker = ZeebeWorker(channel)  # Create a zeebe worker

_username = 'guest'
_amqp_password = 'guest'


async def on_error(exception: Exception, job: Job):
    """
    on_error will be called when the task fails
    """
    print(exception)
    await job.set_error_status(f"Failed to handle job {job}. Error: {str(exception)}")


@worker.task(task_type="run-game", exception_handler=on_error)
async def run_game_task(task_id: str, weapon: str):
    possible_actions = ["камень", "бумага", "ножницы"]
    computer_action = random.choice(possible_actions)
    result = ""

    if weapon == computer_action:
        result += f"Оба игрока выбрали {weapon}. Это ничья!"
    elif weapon == "камень":
        if computer_action == "ножницы":
            result += "Камень ломает ножницы! Ты победил!"
        else:
            result += "Бумага покрывает камень! Ты проиграл."
    elif weapon == "бумага":
        if computer_action == "камень":
            result += "Бумага покрывает камень! Ты победил!"
        else:
            result += "Ножницы режут бумагу! Ты проиграл."
    elif weapon == "ножницы":
        if computer_action == "бумага":
            result += "Ножницы режут бумагу! Ты победил!"
        else:
            result += "Камень ломает ножницы! Ты проиграл."

    data = {
        'task_id': task_id,
        'result': result
    }

    send_to_rabbit(json.dumps(data))

    return {"output": result}


def send_to_rabbit(msg):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ["RABBIT_HOST"], credentials=pika.PlainCredentials(_username, _amqp_password)))
    channel_rabbit = connection.channel()
    channel_rabbit.queue_declare(queue='game_rock')

    channel_rabbit.basic_publish(exchange='',
                                 routing_key='game_rock',
                                 body=msg)
    print(" [x] Sent " + msg)
    connection.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.work())
