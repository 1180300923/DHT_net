import random

class chengzai():
    def __init__(self, n):
        self.count_x = range(40, 500, 20)
        self.n = n
        self.start = 1000

        bw_list = []
        with open('bw.txt', 'r+') as f:
            bw = f.readline()
            count = 1
            while count <= n and bw :
                bw_list.append(int(bw))
                bw = f.readline()
                count+=1
        sorted(bw_list)
        self.bw_list = bw_list

    def update_node_count(self, count_list, path, index):
        for k in range(len(path[index])):
            port = path[index][k]
            count_list[port-self.start] += 1
        return

    def getBw(self,port):
        return self.bw_list[port-1000]

    def get_path_bw(self, count_list, path, index, res):
        bw_once = []
        for k in range(len(path[index])):
            port = path[index][k]
            bw = self.getBw(port)/count_list[port - 1000]
            bw_once.append(bw)
        res.append(min(bw_once))
        return

    def figure_avg_bw(self, path):
        p = []
        count = [0] * self.n
        for i in self.count_x:
            path_index_list = []
            for j in range(i):
                #选中一条路径，对于三种策略而言，其路径的起点终点是一样的，只是经过的节点不一样
                index = random.randint(0, len(path) - 1)
                path_index_list.append(index)
                self.update_node_count(count, path, index)

            res = []
            for index in path_index_list:
                self.get_path_bw(count, path, index, res)
                
            p.append(sum(res)/len(res))
        return p

