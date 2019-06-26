import time,random
import queue,threading
q = queue.Queue()


def Producer(name):
    count =0
    while True:
        time.sleep(random.randrange(3))
        if q.qsize()<3:         # 只要盘子里小于3个包子，厨师就开始做包子
            q.put(count)
            print("Producer %s has produced %s baozi.." %(name,count))
            count += 1

def Consumer(name):
    count =0
    while True:
        time.sleep(random.randrange(4))
        if not q.empty():       # 只要盘子里有包子，顾客就要吃。
            data = q.get()
            print(data)
            print('\033[32;1mConsumer %s has eat %s baozi...\033[0m' % (name,data))
        else:           # 盘子里没有包子
            print("---no baozi anymore----")
        count+=1

p1 = threading.Thread(target=Producer,args=('A',))
c1 = threading.Thread(target=Consumer,args=('B',))
c2 = threading.Thread(target=Consumer,args=('C',))
p1.start()
c1.start()
c2.start()
'''
当你设计复杂程序的时候，就可以用生产者消费者模型，来松耦合你的代码,也可以减少阻塞。
'''