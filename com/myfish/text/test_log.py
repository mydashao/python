import time


LOG = "D:\log.txt"

result=[]
def get_log():
    # logger.debug('     开始读取cookie')
    time.sleep(1)
    with open(LOG, 'r') as f:
        for line in f:
            result.append(line.strip('\n'))
        print(result)

get_log()