# Ting Yao (ty168)
from __future__ import print_function
from heapq import *
import math

ACTIONS = [(0,-1),(-1,0),(0,1),(1,0)]

class Agent:
    def __init__(self, grid, start, goal, type):
        self.grid = grid
        self.previous = {}
        self.explored = []
        self.start = start
        self.grid.nodes[start].start = True
        self.goal = goal
        self.grid.nodes[goal].goal = True
        self.new_plan(type)
    def new_plan(self, type):
        self.finished = False
        self.failed = False
        self.type = type
        if self.type == "RFA":
            self.frontier = []
            xvalue = abs(self.goal[0] - self.start[0])
            yvalue = abs(self.goal[1] - self.start[1])
            self.grid.nodes[self.start].h = (math.sqrt(xvalue * xvalue + yvalue * yvalue))
            self.grid.nodes[self.start].f = self.grid.nodes[self.start].h
            self.costStart = [self.grid.nodes[self.start].f, 0]
            self.costStart.append(self.start)
            heappush(self.frontier, self.costStart)
        if self.type == "MYRFA" or self.type == "RFAG":
            self.frontier = []
            xvalue = abs(self.goal[0] - self.start[0])
            yvalue = abs(self.goal[1] - self.start[1])
            self.grid.nodes[self.start].h = xvalue + yvalue
            self.grid.nodes[self.start].f = self.grid.nodes[self.start].h
            self.costStart = [self.grid.nodes[self.start].f, 0]
            self.costStart.append(self.start)
            heappush(self.frontier, self.costStart)
        if self.type == "RBA":
            self.frontier = []
            xvalue = self.goal[0] - self.start[0]
            yvalue = self.goal[1] - self.start[1]
            self.grid.nodes[self.goal].h = xvalue + yvalue
            self.grid.nodes[self.goal].f = self.grid.nodes[self.goal].h
            self.costStart = [self.grid.nodes[self.goal].f, 0]
            self.costStart.append(self.goal)
            heappush(self.frontier, self.costStart)
    def resultpath(self):
        if self.type == "RFA" or self.type == "MYRFA" or self.type == "RFAG":
            current = self.goal
            while not current == self.start:
                current = self.previous[current]
                self.grid.nodes[current].in_path = True
        if self.type == "RBA":
            current = self.start
            while not current == self.goal:
                current = self.previous[current]
                self.grid.nodes[current].in_path = True
    def astep(self):
        if self.type == "RFA":
            self.RFA()
        if self.type == "MYRFA":
            self.MYRFA()
        if self.type == "RBA":
            self.RBA()
        if self.type == "RFAG":
            self.RFAG()
    def RBA(self):
        if not self.frontier:
            self.failed = True
            print("CANNOT reach goal")
            return
        current = heappop(self.frontier)
        cost = current[1]
        if current[2] in self.explored or current[2] in self.frontier:
            return
        self.grid.nodes[current[2]].checked = True
        self.grid.nodes[current[2]].frontier = False
        self.explored.append(current[2])
        children = [(current[2][0]+a[0], current[2][1]+a[1]) for a in ACTIONS]
        for node in children:
            if node in self.explored or node in self.frontier:
                continue
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                if self.grid.nodes[node].blocked:
                    continue
                else:
                    self.previous[node] = current[2]
                    if node == self.start:
                        self.finished = True
                        print("cost: ", cost+1)
                        return
                    else:
                        manha = abs(self.start[0] - node[0]) + abs(self.start[1] - node[1])
                        costNode = [manha+cost]
                        costNode.append(cost+1)
                        costNode.append(node)
                        heappush(self.frontier, costNode)
                        self.grid.nodes[node].frontier = True
    def RFA(self):
        if not self.frontier:
            self.failed = True
            print("CANNOT reach goal")
            return
        current = heappop(self.frontier)
        cost = current[1]
        if current[2] in self.explored or current[2] in self.frontier:
            return
        self.grid.nodes[current[2]].checked = True
        self.grid.nodes[current[2]].frontier = False
        self.explored.append(current[2])
        children = [(current[2][0]+a[0], current[2][1]+a[1]) for a in ACTIONS]
        for node in children:
            if node in self.explored or node in self.frontier:
                continue
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                if self.grid.nodes[node].blocked:
                    continue
                else:
                    ptr = self.grid.nodes[node]
                    self.previous[node] = current[2]
                    xtemp = abs(self.goal[0] - node[0])
                    ytemp = abs(self.goal[1] - node[1])
                    htemp = (math.sqrt(xtemp*xtemp + ytemp*ytemp))
                    ptr.h = htemp
                    ptr.f = ptr.h + 1
                    if node == self.goal:
                        self.finished = True
                        print("cost: ", cost+1)
                        return
                    else:
                        costNode = [ptr.h+cost]
                        costNode.append(cost+1)
                        costNode.append(node)
                        heappush(self.frontier, costNode)
                        self.grid.nodes[node].frontier = True
    def MYRFA(self):
        if not self.frontier:
            self.failed = True
            print("CANNOT reach goal")
            return
        current = heappop(self.frontier)
        cost = current[1]
        if current[2] in self.explored or current[2] in self.frontier:
            return
        self.grid.nodes[current[2]].checked = True
        self.grid.nodes[current[2]].frontier = False
        self.explored.append(current[2])
        children = [(current[2][0]+a[0], current[2][1]+a[1]) for a in ACTIONS]
        for node in children:
            if node in self.explored or node in self.frontier:
                continue
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                if self.grid.nodes[node].blocked:
                    continue
                else:
                    self.previous[node] = current[2]
                    if node == self.goal:
                        self.finished = True
                        print("cost: ", cost+1)
                        return
                    else:
                        manha = abs(self.goal[0] - node[0]) + abs(self.goal[1] - node[1])
                        costNode = [manha+cost]
                        costNode.append(cost+1)
                        costNode.append(node)
                        heappush(self.frontier, costNode)
                        self.grid.nodes[node].frontier = True
    def RFAG(self):
        if not self.frontier:
            self.failed = True
            print("CANNOT reach goal")
            return
        current = heappop(self.frontier)
        cost = current[1]
        if current[2] in self.explored or current[2] in self.frontier:
            return
        self.grid.nodes[current[2]].checked = True
        self.grid.nodes[current[2]].frontier = False
        self.explored.append(current[2])
        children = [(current[2][0]+a[0], current[2][1]+a[1]) for a in ACTIONS]
        for node in children:
            if node in self.explored or node in self.frontier:
                continue
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                if self.grid.nodes[node].blocked:
                    continue
                else:
                    self.previous[node] = current[2]
                    if node == self.goal:
                        self.finished = True
                        print("cost: ", cost+1)
                        return
                    else:
                        manha = abs(self.goal[0] - node[0]) + abs(self.goal[1] - node[1])
                        costNode = [3*manha+cost]
                        costNode.append(cost+1)
                        costNode.append(node)
                        heappush(self.frontier, costNode)
                        self.grid.nodes[node].frontier = True