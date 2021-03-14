import queue
import threading
import time

'''
作业一：

由 Dijkstra 提出并解决的哲学家就餐问题是典型的同步问题。该问题描述的是五个哲学家共用一张圆桌（如下图所示），分别坐在五张椅子上，在圆桌上有五个盘子和五个叉子，他们的生活方式是交替的进行思考和进餐，思考时不能用餐，用餐时不能思考。平时，一个哲学家进行思考，饥饿时便试图用餐，只有在他同时拿到他的盘子左右两边的两个叉子时才能进餐。进餐完毕后，他会放下叉子继续思考（关于哲学家就餐问题更详细的描述，请参考本节的 PDF 附件，里面有维基百科中的具体描述）。
请写出代码来解决如上的哲学家就餐问题，要求代码返回“当每个哲学家分别需要进食 n 次”时这五位哲学家具体的行为记录（具体需要记录哪些行为，请参考下面的代码）。

复制代码
# 示例代码
import threading
class DiningPhilosophers:
   def __init__(self):
   pass
# philosopher 哲学家的编号。
# pickLeftFork 和 pickRightFork 表示拿起左边或右边的叉子。
# eat 表示吃面。
# putLeftFork 和 putRightFork 表示放下左边或右边的叉子。
   def wantsToEat(self,
      philosopher,
      pickLeftFork(),
      pickRightFork(),
      eat(),
      putLeftFork(),
      putRightFork())
测试用例：

输入：n = 1 （1<=n<=60，n 表示每个哲学家需要进餐的次数。）
预期输出：

[[4,2,1],[4,1,1],[0,1,1],[2,2,1],[2,1,1],[2,0,3],[2,1,2],[2,2,2],[4,0,3],[4,1,2],[0,2,1],[4,2,2],[3,2,1],[3,1,1],[0,0,3],[0,1,2],[0,2,2],[1,2,1],[1,1,1],[3,0,3],[3,1,2],[3,2,2],[1,0,3],[1,1,2],[1,2,2]]
解释:

输出列表中的每一个子列表描述了某个哲学家的具体行为，它的格式如下：
output[i] = [a, b, c] (3 个整数)

a 哲学家编号。
b 指定叉子：{1 : 左边, 2 : 右边}.
c 指定行为：{1 : 拿起, 2 : 放下, 3 : 吃面}。
如 [4,2,1] 表示 4 号哲学家拿起了右边的叉子。所有自列表组合起来，就完整描述了“当每个哲学家分别需要进食 n 次”时这五位哲学家具体的行为记录。
'''

class DiningPhilosophers(threading.Thread):
    def __init__(self, philosopher_number, left_fork, right_fork, operate_queue):
        super().__init__()
        self.philosopher_number = philosopher_number
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.operate_queue = operate_queue
 
    def eat(self):
        global count
        print(f'philosopher: {self.philosopher_number} -> {count}')
        if count > 0:
            count -= 1
        print(f'count -> {count}')
        
        time.sleep(0.01)
        self.operate_queue.put([self.philosopher_number, 0, 3])
 
    def pick_left_fork(self):
        self.operate_queue.put([self.philosopher_number, 1, 1])
 
    def pick_right_fork(self):
        self.operate_queue.put([self.philosopher_number, 2, 1])
 
    def put_left_fork(self):
        self.left_fork.release()
        self.operate_queue.put([self.philosopher_number, 1, 2])
 
    def put_right_fork(self):
        self.right_fork.release()
        self.operate_queue.put([self.philosopher_number, 2, 2])
 
    def run(self):
        print('>>'*20)
        while True:
            left = self.left_fork.acquire(blocking=False)
            right = self.right_fork.acquire(blocking=False)
            if left and right:
                self.pick_left_fork()
                self.pick_right_fork()
                self.eat()
                self.put_left_fork()
                self.put_right_fork()
                break
            elif left and not right:
                self.left_fork.release()
            elif right and not left:
                self.right_fork.release()
            else:
                time.sleep(0.01)
        print(f'philosopher: {self.philosopher_number}吃完')
        print('-+'*20)
 
if __name__ == '__main__':
    operate_queue = queue.Queue()
    fork1 = threading.Lock()
    fork2 = threading.Lock()
    fork3 = threading.Lock()
    fork4 = threading.Lock()
    fork5 = threading.Lock()
    n = 1
    count = 5 * n
    # 假设fork1~fork5的优先级依次降低，让每们哲学家始终先拿优先级高的筷子再拿优先级低的筷子(防死锁)
    for _ in range(n):
        philosopher0 = DiningPhilosophers(0, fork1, fork2, operate_queue)
        philosopher0.start()
        philosopher1 = DiningPhilosophers(1, fork2, fork3, operate_queue)
        philosopher1.start()
        philosopher2 = DiningPhilosophers(2, fork3, fork4, operate_queue)
        philosopher2.start()
        philosopher3 = DiningPhilosophers(3, fork4, fork5, operate_queue)
        philosopher3.start()
        philosopher4 = DiningPhilosophers(4, fork1, fork5, operate_queue)
        philosopher4.start()
    queue_list = []
    for i in range(5 * 5 * n):
        queue_list.append(operate_queue.get())
    print(queue_list)
