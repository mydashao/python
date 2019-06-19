import threading
import time

name_list=[1,2,3,4,5,6,7,8,9,0,11,12,13,14,15,16,17,18,19,20]

def xx():
    lock = threading.Lock()
    threads = []

    for i in range(len(name_list)):
        threads.append(threading.Thread(target=get_ti, args=(name_list[i],lock)))

    for t in threads:
        # t.setDaemon(True)
        print("启动")

        t.start()

def get_ti(name,lock):
    refresh(name,lock)

def refresh(name,lock):
    for i in range(50):

        print(name,":",name*100+i)
        time.sleep(0.1)


xx()
