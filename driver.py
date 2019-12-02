# import ServerTimeout
# from . import ServerTimeout2
# from . import ServerTimeout3
# from . import ServerTimeout4
# from . import ServerTimeout5
# from . import ServerTimeout6
# from . import ServerTimeout7
# from . import ServerTimeout8
# from . import ServerTimeout9
# from . import loadbalancer
# from . import client
import ServerTimeout
import ServerTimeout2
import ServerTimeout3
import ServerTimeout4
import ServerTimeout5
import ServerTimeout6
import ServerTimeout7
import ServerTimeout8
import ServerTimeout9
import loadbalancer
import client
import time
import threading


def main():
    t1 = threading.Thread(target=ServerTimeout.main, name='thread1',args=())
    t2 = threading.Thread(target=ServerTimeout2.main, name='thread2',args=() )
    t3 = threading.Thread(target=ServerTimeout3.main, name='thread3',args=() )
    t4 = threading.Thread(target=ServerTimeout4.main, name='thread4',args=() )
    t5 = threading.Thread(target=ServerTimeout5.main, name='thread5',args=() )
    t6 = threading.Thread(target=ServerTimeout6.main, name='thread6',args=() )
    t7 = threading.Thread(target=ServerTimeout7.main, name='thread7',args=() )
    t8 = threading.Thread(target=ServerTimeout8.main, name='thread8',args=() )
    t9 = threading.Thread(target=ServerTimeout9.main, name='thread9',args=() )
    l1 = threading.Thread(target=loadbalancer.main, name='thread10',args=() )

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    l1.start()

    i=0
    while(i<55):
        c = threading.Thread(target=client.main, name='client'+str(i),args=() )
        c.start()
        time.sleep(1)
        i = i +1



if __name__ == '__main__':
    main()