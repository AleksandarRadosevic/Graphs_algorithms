import operator

import pygame
import os
import config
import json
import sys

class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


class Aki(Agent):
    endFlag = 0;
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [];
        g=Graph(game_map);
        graph=g.get_graph();
        firstNode=game_map[self.row][self.col];
        endNode=game_map[goal[0]][goal[1]];
        visited=set();
        Aki.endFlag=0;
        self.dfs(visited,graph,firstNode,endNode,path);
        return path;

    def dfs(self, visited, graph, node, endNode, path):  # function for dfs
        if (Aki.endFlag==1):
            print("Kraj");
            return;
        if node not in visited:
            print(node.position());
            visited.add(node);
            path.append(node);
            if (endNode==node):
                Aki.endFlag=1;
                print("Kraj");
                return ;
            nextNodes=[];
            for neighbour in graph[node]:
                if neighbour not in visited:
                    object={
                        "node":neighbour,
                        "cost":neighbour.cost(),
                        "direction":int(Graph.check_directionValue(node,neighbour))
                    };
                    nextNodes.append(object);
            nextNodes=sorted(nextNodes,key=lambda k: (int(k["cost"]),int(k["direction"])));
            while(len(nextNodes)>0):
                next=nextNodes.pop(0);
                self.dfs(visited,graph,next["node"],endNode,path);
                if (Aki.endFlag==1):
                    return;
                path.pop();

class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        g=Graph(game_map);
        graph=g.get_graph();
        firstNode=game_map[self.row][self.col];
        endNode=game_map[goal[0]][goal[1]];
        visited=[];
        path=self.bfs(visited,graph,firstNode,endNode);
        return path;

    def calculatePassability(self,node,graph,temp):
        s=0;
        i=0;
        for neighbour in graph[node]:
            if (neighbour==temp):
                continue;
            s+=neighbour.cost();
            i=i+1;
        s=s/i;
        return s;

    def nodesNext(self,graph,node,nodesNext):
        nodes=[];
        i=0;
        for neighbour in nodesNext:
            object={
                "node":i,
                "val":float(self.calculatePassability(neighbour,graph,node)),
                "direction":int(0)
            };
            c=Graph.check_direction(node, neighbour);
            if (c=='n'):
                object["direction"] = 0;
            elif (c=='e'):
                object["direction"] = 1;
            elif (c=='s'):
                object["direction"] = 2;
            else:
                object["direction"] = 3;
            nodes.append(object);
            i = i + 1;
        nodes=sorted(nodes,key=lambda k: (float(k["val"]),int(k["direction"])));
        i=0;
        nodes2=[None ]* len(nodesNext);
        for n in nodes:
            print(nodesNext[n["node"]].position());
            nodes2[i]=nodesNext[n["node"]];
            i+=1;
        return nodes2;


    def bfs(self,visited, graph, node,endNode):  # function for BFS
        queue = []
        # push the first path into the queue
        queue.append([node]);
        visited.append(node);
        paths=[];
        while len(queue)>0:  # Creating loop to visit each node
            path = queue.pop(0);
            # get the last node from the path
            m = path[-1];
            print(m, end=" ")
            if (m == endNode):
                print("Uspeh");
                paths.append(path);
                continue;
            nextNodes=[];
            for neighbour in graph[m]:
                if neighbour not in visited:
                    visited.append(neighbour)
                    nextNodes.append(neighbour);
            nextNodes=self.nodesNext(graph,m,nextNodes);
            for neighbour in nextNodes:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
        if len(paths)==1:
            print("Postoji jedna putanja");
            return paths[0];
        # else:
        #     print("Postoji vise putanja");
        #     maxSum=9223372036854775807;
        #     minPath=None;
        #     for path in paths:
        #         sum=0;
        #         for node in path:
        #             sum+=node.cost();
        #         if sum<maxSum:
        #             maxSum=sum;
        #             minPath=path;
        #     return minPath;

class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def nodesNext(self,graph,node,nodesNext):
        nodes=sorted(nodesNext,key=lambda k: (int(k["cost"]),int(k["nodes_number"])));
        return nodes;

    def get_agent_path(self, game_map, goal):
        g=Graph(game_map);
        graph=g.get_graph();
        firstNode=game_map[self.row][self.col];
        endNode=game_map[goal[0]][goal[1]];
        visited=[];
        path=self.branch_and_bound(visited,graph,firstNode,endNode);
        return path;

    def branch_and_bound(self,visited, graph, node,endNode):  # function for BFS
        queue = []
        # push the first path into the queue
        n=node;
        obj = {
            "path": [n],
            "cost": node.cost(),
            "nodes_number": 1
        };
        queue.append(obj);
        visited.append(n);
        while len(queue)>0:  # Creating loop to visit each node
            path = queue.pop(0);
            # get the last node from the path

            m = path["path"][-1];
            visited.append(m);
            #print(f'Cvor {m.position()} cena {path["cost"]}');
            #print(m, end=" ")
            if (m == endNode):
                return path["path"];
            nextNodes=[];
            for neighbour in graph[m]:
                    if neighbour in visited:
                        continue;

                    nextNodes.append(neighbour);
            for neighbour in nextNodes:
                new_path = list(path["path"]);
                new_path.append(neighbour);
                obj={
                    "path":list(new_path),
                    "cost":int(path["cost"]+neighbour.cost()),
                    "nodes_number":int(path["nodes_number"]+1)
                };
                queue.append(obj);
                queue=sorted(queue,key=lambda k: (int(k["cost"]),int(k["nodes_number"])));

class Bole(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def nodesNext(self,nodesNext):
        nodes=sorted(nodesNext,key=lambda k: (int(k["cost"]),int(k["nodes_number"])));
        return nodes;

    def get_agent_path(self, game_map, goal):
        g=Graph(game_map);
        graph=g.get_graph();
        h=Graph.heuristics(game_map,game_map[goal[0]][goal[1]]);
        firstNode=game_map[self.row][self.col];
        endNode=game_map[goal[0]][goal[1]];

        visited=[];
        path=self.a_star(visited,graph,firstNode,endNode,h);
        return path;

    def a_star(self,visited, graph, node,endNode,h):  # function for BFS
        queue = []
        # push the first path into the queue
        n=node;
        obj = {
            "path": [n],
            "cost": node.cost(),
            "nodes_number": int(1),
            "val":int(0)
        };
        queue.append(obj);
        visited.append(n);
        while len(queue)>0:  # Creating loop to visit each node
            path = queue.pop(0);
            # get the last node from the path

            m = path["path"][-1];
            visited.append(m)
            print(f'Cvor {m.position()} cena {path["cost"]-path["val"]}');

            path["cost"]-=path["val"];
            #print(f'Cvor {m.position()} cena {path["cost"]}');

            #print(m, end=" ")
            if (m == endNode):
                return path["path"];
            nextNodes=[];
            for neighbour in graph[m]:
                    if neighbour in visited:
                        continue;
                    nextNodes.append(neighbour);
            for neighbour in nextNodes:
                new_path = list(path["path"]);
                new_path.append(neighbour);
                val=h[neighbour.position()];
                obj={
                    "path":list(new_path),
                    "cost":int(path["cost"]+neighbour.cost())+val,
                    "nodes_number":int(path["nodes_number"]+1),
                    "val":val
                };
                queue.append(obj);
                queue=sorted(queue,key=lambda k: (int(k["cost"]),int(k["nodes_number"])));
class Graph():
    def __init__(self,game_map):
        self.graph = {};
        self.vertices_no = 0;
        for row in range(len(game_map)):
            for col in range(len(game_map[row])):
                self.add_vertex(game_map[row][col]);
        for node in self.graph:
            position=node.position();
            row=position[0];
            col=position[1];
            try:
                if (col==0):
                    raise Exception;
                left=game_map[position[0]][position[1]-1];
                self.add_edge(node,left);
            except:
                pass
            try:
                if (col+1==(len(game_map[row]))):
                    raise Exception;
                right=game_map[position[0]][position[1]+1];
                self.add_edge(node, right);
            except:
                pass

            try:
                if (row+1==len(game_map)):
                    raise Exception;
                down=game_map[position[0]+1][position[1]];
                self.add_edge(node, down);
            except:
                pass
            try:
                if (row==0):
                    raise Exception;
                up=game_map[position[0]-1][position[1]];
                self.add_edge(node, up);
            except:
                pass
    def add_edge(self,v1, v2):
        # Check if vertex v1 is a valid vertex
        if v1 not in self.graph:
            print("Vertex ", v1, " does not exist.")
        # Check if vertex v2 is a valid vertex
        elif v2 not in self.graph:
            print("Vertex ", v2, " does not exist.")
        else:
            # Since this code is not restricted to a directed or
            # an undirected graph, an edge between v1 v2 does not
            # imply that an edge exists between v2 and v1
            self.graph[v1].append(v2)
    def add_vertex(self,v):
        if v in self.graph:
            print("Vertex ", v, " already exists.")
        else:
            vertices_no = self.vertices_no + 1
            self.graph[v] = []
    def print_graph(self):
        for vertex in self.graph:
            for edges in self.graph[vertex]:
                print(vertex.position(), " -> ", edges[0], " edge weight: ", edges[0].cost())
    def get_graph(self):
        return self.graph;

    @staticmethod
    def heuristics(game_map,endNode):
        map={};
        position1 = endNode.position();
        for row in range(len(game_map)):
            for col in range(len(game_map[row])):
                node=game_map[row][col];
                position2=node.position();
                val=abs(position1[0]-position2[0])+abs(position1[1]-position2[1]);
                map[(position2[0],position2[1])]=val;
        return map;


    @staticmethod
    def nextNode(node1,nodes):
        tempNode=nodes[0];
        bestWay=Graph.check_direction(node1,nodes[0]);
        for node in nodes:
            direction=Graph.check_direction(node1,node);
            print(f"Put {direction}")
            if (direction=='n'):
                return node;
            elif (direction=='e'):
                bestWay='e';
                tempNode=node;
            elif (direction=='s' and bestWay=='w'):
                bestWay='s';
                tempNode=node;
        print(f"Najbolji put je {bestWay} ");
        return tempNode;

    @staticmethod
    def check_direction(node1,node2):
        position1=node1.position();
        position2=node2.position();
        if (position2[0]-position1[0]==1):
            return 's';
        elif (position2[0]-position1[0]==-1):
            return 'n';
        elif (position2[1]-position1[1]==1):
            return 'e';
        return 'w';

    @staticmethod
    def check_directionValue(node1,node2):
        position1=node1.position();
        position2=node2.position();
        if (position2[0]-position1[0]==1):
            return 2;
        elif (position2[0]-position1[0]==-1):
            return 0;
        elif (position2[1]-position1[1]==1):
            return 1;
        return 3;
class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

