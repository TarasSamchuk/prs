import time

import hazelcast
from hazelcast.config import Config
from hazelcast import HazelcastClient
from threading import Thread
def time_of_function(function):
    def wrapped(*args):
        start_time = time.perf_counter()
        res = function(*args)
        print("Time: ", time.perf_counter() - start_time)
        return res
    return wrapped

@time_of_function
def add_threads():
    client = hazelcast.HazelcastClient(
        cluster_name = "dev",
        cluster_members = ["127.0.0.1"]
    )
    multi_map = client.get_multi_map("my-distributed-map").blocking()

    multi_map.put("my-key", "value1")
    multi_map.put("my-key", "value2")
    multi_map.put("my-key", "value3")

    # values = multi_map.get("my-key")
    # print(values)
    #
    # multi_map.remove("my-key", "value2")

@time_of_function
def pessimistic_locking():
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("my-distributed-map").blocking()

    key = "1"
    distributed_map.put(key, 0)

    print("Starting pessimistic locking")

    for i in range(1000):
        distributed_map.lock(key)
        try:
            value = distributed_map.get(key)
            value += 1
            distributed_map.put(key, value)
        finally:
            distributed_map.unlock(key)
    print("Finished! \n Result = ", distributed_map.get(key))

@time_of_function
def locking_maps():
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("map").blocking()

    key = "1"
    distributed_map.put(key, 0)

    print("Starting locking")
    for i in range(1000):
        if i % 100 == 0:
            value = distributed_map.get(key)
            value += 1
            distributed_map.put(key, value)
    print("Finished! \n Result = ", distributed_map.get(key))

@time_of_function
def optimistic_locking():
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("my-distributed-map").blocking()

    key = "1"
    distributed_map.put(key, 0)
    print("Starting optimist locking")
    for i in range(1000):
        if i % 10:
            while True:
                value = distributed_map.get(key)
                new_value = value + 1
                distributed_map.put(key, value)
                if distributed_map.replace_if_same(key, value, new_value):
                    break;
    print("Finished! \n Result = ", distributed_map.get(key))

def test():
    client = hazelcast.HazelcastClient()
    my_map = client.get_map("my-distributed-map")


    for i in range(1000):
        my_map.put(i, "value-{}".format(i))
        print(i)

    client.shutdown()

def bounded_queue():
    client = hazelcast.HazelcastClient()

    queue = client.get_queue("my-bounded-queue").get_bounded_queue(1000)

    queue.put("Hello, World!")

    element = queue.take()
    print(element)

    queue = client.get_queue("my-bounded-queue").get_bounded_queue(1000, fair=False)

def run_app(type_lockiing):
    thread = Thread(target=type_lockiing)
    thread2 = Thread(target=type_lockiing)
    thread3 = Thread(target=type_lockiing)

    thread3.start()
    thread2.start()
    thread.start()
    
    print("===========================================================")

if __name__ == "__main__":
    # add_threads()
    # locking_maps()
    # pessimistic_locking()
    # optimistic_locking()
    # bounded_queue()
    run_app(add_threads)
    run_app(locking_maps)
    run_app(pessimistic_locking)
    run_app(optimistic_locking)
# client = HazelcastClient(

#     cluster_members=[
#         "localhost:5701",
#         "localhost:5702",
#         "localhost:5703"
#     ]
# )
#
#
# config = Config()
# config.set_backup_count(2)
#
# client = HazelcastClient(config=config)
#
#
#
# my_map = client.get_map("my-distributed-map")
#
# for i in range(1000):
#     my_map.put(i, "value-{}".format(i))
#     print(i)
#
# client.shutdown()

