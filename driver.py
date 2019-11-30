import server1
import loadbalancer
import client
import time
import threading
from threading import Thread

Thread(target=server1.server_process()).start()
# time.sleep(5)
print ('server completed')
Thread(target=loadbalancer.loadbal_process()).start()
time.sleep(5)
print ('lb completed')
Thread(target=client.client_process()).start()
print ('cleint completed')

print(threading.current_thread().getName(), 'Exiting')