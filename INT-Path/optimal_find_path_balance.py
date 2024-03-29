# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import copy
import random
import networkx as nx
import numpy as np
import time
import randomTopo
import FixedOddTopo
import  OddEdge
import specialTopo
class Graph(object):
	def __init__(self, *args, **kwargs):
		self.node_neighbors = {}
		self.visited = {}
		self.A = []  # 为现存节点数组
		self.degree = []  # 为度数组

	def add_nodes(self, nodelist):
		for node in nodelist:
			self.add_node(node)

	def add_node(self, node):
		if not node in self.nodes():
			self.node_neighbors[node] = []

	def add_edge(self, edge):
		u, v = edge
		if (v not in self.node_neighbors[u]) and (u not in self.node_neighbors[v]):
			self.node_neighbors[u].append(v)

			if (u != v):
				self.node_neighbors[v].append(u)

	def nodes(self):
		return self.node_neighbors.keys()

	def not_null_node(self):
		self.A.clear()
		for node in self.nodes():
			if len(self.node_neighbors[node]) > 0:
				self.A.append(node)

	def degrees(self):
		self.degree.clear()
		Node = self.nodes()
		for node in Node:
			self.degree.append(len(self.node_neighbors[node]))

	def set_diff(self, nodes):
		others = []
		for node in self.A:
			if node not in nodes:
				others.append(node)

		return others

	def F1(self):  # 求所有联通子图
		nodes = []
		visited = []
		subgraph = {}
		i = 1
		temp = self.set_diff(nodes)
		while len(temp) > 0:
			order = self.depth_first_search(temp[0])
			subgraph[i] = order
			i += 1
			visited.extend(order)
			temp = self.set_diff(visited)
		return subgraph

	def judge(self, subgraph):
		for i in subgraph:
			t = 0
			temp = subgraph[i]
			for node in temp:
				if self.degree[node - 1] % 2 != 0:
					t = 1  # t=1说明有奇顶点
					break
			if t == 0:
				return i
		return 0

	def F2(self, gt):
		num = 0
		for node in gt:
			if self.degree[node - 1] % 2 != 0:
				num += 1
		return num

	def F3(self, path):
		for i in range(len(path) - 1):
			self.node_neighbors[path[i]].remove(path[i + 1])
			self.node_neighbors[path[i + 1]].remove(path[i])
		self.not_null_node()

	def depth_first_search(self, root=None):  # 在连通的前提下进行深度优先搜索
		order = []

		def dfs(node):
			self.visited[node] = True
			order.append(node)
			for n in self.node_neighbors[node]:
				if not n in self.visited:
					dfs(n)

		if root:
			dfs(root)

		for node in self.nodes():
			if not node in self.visited:
				for v_node in self.visited:
					if node in self.node_neighbors[v_node]:
						dfs(node)
		self.visited.clear()
		return order

	def my_path(self, subgraph):
		odd_node = []
		path_len={}
		for node in subgraph:
			if self.degree[node - 1] % 2 != 0:
				odd_node.append(node)
		distances = {}
		g_temp = dict_copy(self.node_neighbors, subgraph)
		for i in list(g_temp.keys()):
			temp = []
			for j in g_temp[i]:
				temp.append((j, 1))
			distances[i] = temp
		for node in odd_node:
			current = node
			dis=copy.deepcopy(distances)
			d, paths = dijkstra(dis, current)
			use_dict = dict_copy(paths, odd_node)
			d = dict_copy(d, odd_node)
			n_max = max(d.items(), key=lambda x: x[1])[0]
			path_len[d[n_max]]=use_dict[n_max]
		return max(path_len.items(), key=lambda x: x[0])[1]

def dijkstra(G, s):
	d = {}  # node distances from source
	predecessor = {}  # node predecessor on the shortest path

	# initing distances to INF for all but source.
	for v in G:
		if v == s:
			d[v] = 0
		else:
			d[v] = float("inf")

	predecessor[s] = None

	Q = list(G.keys())  # contains all nodes to find shortest paths to, intially everything.
	while (Q):  # until there is nothing left in Q
		u = min(Q, key=d.get)  # get min distance node
		Q.remove(u)
		for v in G[u]:  # relax all outgoing edges from it
			relax(u, v, d, predecessor)

		# print(d)
		# print(predecessor)
		paths = {}
	for v in predecessor:
		paths[v] = [v]
		p = predecessor[v]
		while p is not None:
			# paths[v] +=""+p
			paths[v].append(p)
			p = predecessor[p]
	# for v, path in paths.items():
	# 	print(v, path)
	return d, paths


def relax(u, v, d, predecessor):
	weight = v[1]
	v = v[0]
	if d[v] > d[u] + weight:
		d[v] = d[u] + weight
		predecessor[v] = u


def add_path(p1, p2):
	k=1
	for i in range(len(p2)-1):
		p1.insert(p1.index(p2[0])+k,p2[i+1])
		k+=1
	return p1


def dict_copy(dict, a):
	temp = {}
	for i in a:
		temp[i] = dict[i]
	return temp


'''
    is_connected - Checks if a graph in the form of a dictionary is 
    connected or not, using Breadth-First Search Algorithm (BFS)
'''


def is_connected(G):
	start_node = list(G)[0]
	color = {v: 'white' for v in G}
	color[start_node] = 'gray'
	S = [start_node]
	while len(S) != 0:
		u = S.pop()
		for v in G[u]:
			if color[v] == 'white':
				color[v] = 'gray'
				S.append(v)
			color[u] = 'black'
	return list(color.values()).count('black') == len(G)


'''
    odd_degree_nodes - returns a list of all G odd degrees nodes
'''


def odd_degree_nodes(G):
	odd_degree_nodes = []
	for u in G:
		if len(G[u]) % 2 != 0:
			odd_degree_nodes.append(u)
	return odd_degree_nodes


'''
    from_dict - return a list of tuples links from a graph G in a 
    dictionary format
'''


def from_dict(G):
	links = []
	for u in G:
		for v in G[u]:
			links.append((u, v))
	return links


'''
    fleury(G) - return eulerian trail from graph G or a 
    string 'Not Eulerian Graph' if it's not possible to trail a path
'''


def fleury(G):
	'''
		checks if G has eulerian cycle or trail
	'''
	odn = odd_degree_nodes(G)
	if len(odn) > 2 or len(odn) == 1:
		return 'Not Eulerian Graph'
	else:
		g = copy.deepcopy(G)
		trail = []
		if len(odn) == 2:
			u = odn[0]
		else:
			u = list(g)[0]
		while len(from_dict(g)) > 0:
			current_vertex = u
			for u in g[current_vertex]:
				g[current_vertex].remove(u)
				g[u].remove(current_vertex)
				bridge = not is_connected(g)
				if bridge:
					g[current_vertex].append(u)
					g[u].append(current_vertex)
				else:
					break
			if bridge:
				g[current_vertex].remove(u)
				g[u].remove(current_vertex)
				g.pop(current_vertex)
			if (len(trail) == 0):
				trail.append(current_vertex)
				trail.append(u)
			else:
				trail.append(u)
	#print(trail)
	return trail

def euler(G,start=None):
	path = []
	g=copy.deepcopy(G)
	def hierholzer(node):
		if (len(g[node]) == 0):
			path.append(node)
			return
		for n in g[node]:
			g[node].remove(n)
			g[n].remove(node)
			hierholzer(n)
			if (len(g[node]) == 0):
				path.append(node)
				return
	odn = odd_degree_nodes(g)
	if len(odn) > 2 or len(odn) == 1:
		return 'Not Eulerian Graph'
	else:
		if start:
			u=start
		else:
			if len(odn) == 2:
				u = odn[0]
			else:
				u = list(g)[0]
		hierholzer(u)
	path.reverse()
	#print(path)
	return path

def path_iden(Queue,g):	#找出Queue中哪条路径应该与g相连
	for n in g:
		for path in Queue:
			if(n in path):
				Queue.remove(path)
				return path,n

def verification(Queue,testG):
	for path in Queue:
		for i in range(len(path)-1):
			testG[path[i]].remove(path[i+1])
			testG[path[i+1]].remove(path[i])
			i+=1
	#print('ok')

def find_path(G):
	num_fleury = 0
	num_path = 0
	g = Graph()
	g.add_nodes([i + 1 for i in range(len(G))])
	for i in range(len(G)):
		for j in range(len(G[i])):
			if G[i][j] != 0:
				g.add_edge((i + 1, j + 1))
	g.not_null_node()
	g.F1()
	testG=copy.deepcopy(g.node_neighbors)
	Queue = []
	while (len(g.A) > 0):
		g.degrees()
		subgraph = g.F1()
		n = len(subgraph)
		T = g.judge(subgraph)
		if (T > 0):
			if (len(Queue) > 0):
				t_path,start = path_iden(Queue,subgraph[T])
				g_temp = dict_copy(g.node_neighbors, subgraph[T])
				#result = fleury(g_temp)
				result =euler(g_temp,start)
				num_fleury += 1
				g.F3(result)
				#print('r',result)
				#print('p',t_path)
				#print('Q',Queue)
				result = add_path(t_path, result)
				#print('rs',result)
				Queue.append(result)
			else:
				g_temp = dict_copy(g.node_neighbors, subgraph[T])
				#t_path = fleury(g_temp)
				t_path = euler(g_temp)
				num_fleury += 1
				Queue.append(t_path)
				g.F3(t_path)
			continue
		for i in range(1, n + 1):
			odd_num = g.F2(subgraph[i])
			if odd_num == 2:
				g_temp = dict_copy(g.node_neighbors, subgraph[i])
				#path = fleury(g_temp)
				path = euler(g_temp)
				num_fleury += 1
			elif odd_num > 2:
				path = g.my_path(subgraph[i])  #mypath函数改写了
			else:
				break
			Queue.append(path)
			g.F3(path)
	num_path = len(Queue)
	#print('queue', Queue)
	verification(Queue,testG)
	return num_fleury, num_path, Queue


def g_generator(NUM_GRAPHS, NUM_NODES):
	# NUM_GRAPHS = 25
	# NUM_NODES = 500
	op = []

	for i in range(NUM_GRAPHS):
		while (True):
			#节点数  每个节点与2个临近的结点连接在环形拓扑中  重新连接每条边的概率
			WS = nx.random_graphs.connected_watts_strogatz_graph(NUM_NODES, 2,
																 random.uniform(i * 2 / NUM_NODES - 0.1,
																				i * 2 / NUM_NODES))
			# spring layout
			count = 0
			#计算奇数顶点的数目
			for node in range(NUM_NODES):
				if WS.degree(node) % 2 != 0:
					count += 1

			if count == i * 2:
				network_matrix = np.zeros([NUM_NODES, NUM_NODES])

				for edge in WS.edges():
					network_matrix[edge[0]][edge[1]] = 1
				print(network_matrix)
				nx.draw(WS)
				plt.show()
				op.append(network_matrix)
				break
	return op

def variance(Q):
	l=[]
	sum=0
	var=0
	for _ in Q:
		l.append(len(_))
		sum+=len(_)
	average=sum/len(Q)
	for _ in l:
		var+=pow(_-average,2)
	var/=len(Q)
	return var
'''
	#第一个图100个测试数据
	for i in range(100):
		sNum = i
		topoMatrix,oddCount= randomTopo.createRandomTopo(sNum)
		num_fleury, num_path,q= find_path(topoMatrix)
		print(num_path)
'''
'''
	#第二个图数据采集
	for i in range(40,150):
		topoMatrix=FixedOddTopo.FixedoddTopo(i,20)
		num_fleury, num_path,q= find_path(topoMatrix)
		print(num_path)
'''
'''
	#第三个图采集750组数据 固定39个顶点 奇数顶点
	for i in range(750):
		if(i<=39*38/2):
			topoMatrix = OddEdge.Oddedge(39,i)
			num_fleury, num_path, q = find_path(topoMatrix)
			print(num_path)
'''
'''
	#第四个图采集30组数据  用随机拓扑测试
	op = g_generator(3, 29)
	for _ in op:
		start = time.clock()
		num_fleury, num_path,q= find_path(_)
		end = time.clock()
		print("INT路径数是：",num_path)
		print("路径为：",q)
		print(len(q[0]) - 1)
		print(len(q[num_path - 1]) - 1)
'''
'''
	#第六个图数据采集
	for i in range(20,120):
		#CPU的折行时间
		start = time.clock()
		topoMatrix=FixedOddTopo.FixedoddTopo(i,20)
		num_fleury, num_path,q= find_path(topoMatrix)
		end = time.clock()
		print(end-start)
'''
'''
	#第七个图数据采集 任何图度数为奇数顶点的个数是偶数
	for i in range(0,250):
		#偶数
		if(i%2==0):
			#没办法500个顶点
			topoMatrix=FixedOddTopo.FixedoddTopo(500,i)
			start = time.clock()
			num_fleury, num_path,q= find_path(topoMatrix)
			end = time.clock()
			print(end-start)
	for i in range(0,250):
		#偶数
		if(i%2==0):
			#没办法500个顶点
			topoMatrix=FixedOddTopo.FixedoddTopo(500,i)
			num_fleury, num_path,q= find_path(topoMatrix)
			print(num_fleury)	
'''
'''
	#最后一部分工作 Fattree  sNum必须是大于10  5的倍数
	for i in range(2,21):
		topoMatrix = specialTopo.genFatTree(i*5)
		#print(topoMatrix)
		num_fleury, num_path,q= find_path(topoMatrix)
		print(num_path)

'''
'''
	#最后一部分工作 LeafSpine  sNum必须是大于3  3的倍数
	for i in range(1,34):
		topoMatrix = specialTopo.genSpineLeaf(i*3)
		#print(topoMatrix)
		num_fleury, num_path,q= find_path(topoMatrix)
		print(num_path)

'''
if __name__ == '__main__':
	#最后一部分工作 LeafSpine  sNum必须是大于3  3的倍数
	topo, oddCount= randomTopo.createRandomTopo(20)
	num_fleury, num_path, q= find_path(topo)
	# print(num_path)
	# print(topoMatrix)
	# print(q)

	# 写入topo
	with open('topo.txt', 'w') as f:
		n = len(topo)
		m = len(topo[0])
		for i in range(n):
			for j in range(m):
				if i < j and topo[i][j] == 1:
					f.write('{} {}\n'.format(i, j))
	
	# 写入path
	with open('path.txt', 'w') as f:
		for path in q:
			n = len(path)
			for i in range(n - 1):
				f.write('{} {} '.format(path[i]-1, path[i+1]-1))
			f.write('\n')
