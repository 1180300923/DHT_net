import hashlib
import numpy as np
import random
import xlwt
from chengz import chengzai
import hashlib

class hashNode:
    def __init__(self, hash_value, ip_and_port, port, bw):
        self.id = hash_value
        self.ip_and_port = ip_and_port
        self.port = port
        self.buckets = [None] * digit_count
        self.bw = bw
        
    def get_bucket(self, node_id):
        self_id = self.id
        leading_zero = 0

        for i in range(len(self_id)):
            diff = ord(self_id[i]) ^ ord(node_id[i]) 
            if diff == 0:
                leading_zero += hex_count
            else:
                hex1, hex2 = map_to_hex[self_id[i]], map_to_hex[node_id[i]]
                for j in range(hex_count):
                    if hex1[j] != hex2[j]:
                        leading_zero += 1
                break

        distance = digit_count - leading_zero
        return distance
    
    def put_node(self, distance, node):
        if self.buckets[distance] is None:
            self.buckets[distance] = []
        self.buckets[distance].append(node)
        return
    
    def str_node(self):
        return str(self.id) + "@" + str(self.ip_and_port)

host = "127.0.0.1"
start = 1000
n = 100
digit_count = 160
hex_count = 4
precent = 0.1
map_to_hex = {  '0' : "0000", '1' : "0001", '2' : "0010", '3' : "0011",
                '4' : "0100", '5' : "0101", '6' : "0110", '7' : "0111",
                '8' : "1000", '9' : "1001", 'a' : "1010", 'b' : "1011",
                'c' : "1100", 'd' : "1101", 'e' : "1110", 'f' : "1111"}
index_count = [0] * n
paths = []
#bw_list = [83369, 65847, 61649, 60932, 57335, 49324, 48113, 47785, 47501, 46775, 44075, 43240, 36361, 33668, 32900, 32806, 31754, 31743, 31014, 30312, 28678, 26994, 24546, 22907, 20841, 20642, 20459, 19536, 18994, 17730, 15995, 13560, 12324, 11881, 11804, 11749, 11742, 11485, 11038, 10879, 10656, 10284, 10275, 10163, 10145, 9970, 9692, 9250, 9097, 9042, 8885, 8072, 6832, 6763, 6208, 6199, 6185, 6130, 5793, 5509, 5350, 5302, 5034, 4772, 4731, 4305, 3876, 3635, 3532, 3211, 2647, 2569, 2559, 2519, 2331, 2281, 2203, 2022, 1879, 1772, 1598, 1316, 1221, 1212, 1200, 1115, 1010, 927, 920, 716, 692, 625, 399, 331, 226, 126, 114, 113, 108, 81]
def get_bw():
    bw_list = []
    with open('bw.txt', 'r+') as f:
        bw = f.readline()
        count = 1
        while count <= n and bw :
            bw_list.append(int(bw))
            bw = f.readline()
            count+=1
    sorted(bw_list)
    return bw_list  
bw_list = get_bw()


def weighted_choice(weights):
  rnd = random.random() * sum(weights)
  for i, w in enumerate(weights):
      rnd -= w
      if rnd < 0:
          return i
def get_level(bw):
    if bw <= 500:
        return 3
    elif bw > 500 and bw <= 1000:
        return 2
    elif bw > 1000 and bw <= 2000:
        return 1
    else:
        return 0

def get_avg(bw_list):
    if len(bw_list) == 0:
        return 0
    return sum(bw_list)/len(bw_list)


def find_node(target, source, path):
    #print(" step %d: %s" % (count, source.str_node()))
    if source.id == target:
        return 0
    else:
        distance = source.get_bucket(target)
        bucket = source.buckets[distance]
        if len(path) >= n or bucket is None or len(bucket) == 0:
            return n
        for item in bucket:
            if item.id == target:
                next_node = item
                index_count[next_node.port - start] += 1
                path.append(next_node.port)
                return find_node(target, next_node, path) + 1

        if True:
            #带宽加权策略            
            blist = []
            for node_index in range (len(bucket)):
                node = bucket[node_index]
                #防止产生重复节点
                if node.port not in path:
                    blist.append(node.bw)
                else:
                    blist.append(0)
            if sum(blist) == 0:
                return n
            next_index = weighted_choice(blist)
            

            #分组带宽加权策略
            # level_node = [[],[],[],[]]
            # level_bw   = [[],[],[],[]]
            # for node_index in range (len(bucket)):
            #     node = bucket[node_index]
            #     #防止产生重复节点
            #     if node.port not in path:
            #         level_index = get_level(node.bw)
            #         level_node[level_index].append(node_index)
            #         level_bw[level_index].append(node.bw)
            # next_level = weighted_choice([get_avg(level_bw[0]), get_avg(level_bw[1]), get_avg(level_bw[2]), get_avg(level_bw[3])])
            # next_index = level_node[next_level][random.randint(0, len(level_node[next_level])- 1)]
            #随机选择策略
            
            # next_list = []
            # for node_index in range (len(bucket)):
            #     node = bucket[node_index]
            #     #防止产生重复节点
            #     if node.port not in path:
            #         next_list.append(node_index)
                
            # if len(next_list) == 0:
            #     return n
            # next_index = next_list[random.randint(0, len(next_list)- 1)]
            
    
            next_node = bucket[next_index]
            index_count[next_node.port - start] += 1
            path.append(next_node.port)
            return find_node(target, next_node, path) + 1

def getID(hash512, ip_and_port, n):
    hash512.update(ip_and_port.encode("utf-8"))
    orig_hash = hash512.hexdigest()
    start = random.randint(0, len(orig_hash)- n/4 - 1)
    return orig_hash[start:start+n//4]
    
def figure_avg(path, n):
    sum_path_length = 0
    sum_path_count = 0
    flag = True      
    mid = 0

    max_count, index = 0, 0
    longest_index = 0
    for i in range(len(path)):
        sum_path_count += path[i]
        sum_path_length += i * path[i]

        if flag and sum_path_count > n * (n-1)/2:
            mid = i
            flag = False
        
        if path[i] != 0:
            longest_index = i

        if max_count < path[i]:
            max_count, index = path[i], i

    return sum_path_length, sum_path_count, (n*(n-1)-sum_path_count)/(n*(n-1)), sum_path_length/sum_path_count, mid, index, longest_index

if __name__ == '__main__':
    hash512 = hashlib.sha512()
    hash_node_list = []

    for port in range( start, start + n):
        ip_and_port = host + ":" + str(port)

        bw = 0
        if port - start < len(bw_list):
            bw = bw_list[port - start]
        
        #获取固定位数的ID
        node_id = getID(hash512, ip_and_port, digit_count)

        hash_node = hashNode( node_id, ip_and_port, port, bw)
        hash_node_list.append( hash_node)

        for j in range(port - start):  
            old_node = hash_node_list[j]
            distance = hash_node.get_bucket(old_node.id)

            #节点信息掌握度
            if random.random() < precent:
                old_node.put_node(distance, hash_node)
            if random.random() < precent:
                hash_node.put_node(distance, old_node)
    
    results = [0] * (n+1)
    steps = np.zeros((n,n), dtype = np.int)
    for i in range(n):
        source_node = hash_node_list[i]
        for j in range(n):
            if i == j:
                continue
            path = [source_node.port]
            step_count = find_node(hash_node_list[j].id, source_node, path)
            if step_count >= n :
                continue
            paths.append(path)
            steps[i][j], steps[j][i] = step_count, step_count
            results[step_count] += 1
        

    print("%d 个节点, ID %d 位" %(n, digit_count))
    print(results)
    print(figure_avg(results, n))

    cz = chengzai(n)
    print(cz.figure_avg_bw(paths))
