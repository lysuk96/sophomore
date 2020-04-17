import csv
import sys
import pickle


class Node(object) :
    '''
    Non-leaf node
         m: # of keys
         p: an array of b <key, left_child_node> pairs
         r: a pointer to the rightmost child node
    Leaf node
         m: # of keys
         p: an array of b <key, value(or pointer to the value)> pairs
         r: a pointer to the right sibling node
    '''
    def __init__(self, m):
        self.m = m
        self.p = [] # key : p[n][0] , value || pointer : p[n][1]
        self.r = None

        self.leaf = True
        self.parent = None

    def is_full(self) :
        if len(self.p) == self.m :
            return True
        elif len(self.p) > self.m :
            print ("fatal error")
        return False

    def add(self, key, value): 
        # some : left_child or value(or pointer to the value)
        if len(self.p) == 0 :
            self.p.append([key, value])
        
        else :
            #find the right place and put in
            if key < self.p[0][0] :
                self.p.insert(0, [key, value])
            elif key > self.p[len(self.p)-1][0] :
                self.p.insert(len(self.p), [key, value])
            else :
                for i in range(0, len(self.p) - 1) :
                    if (self.p[i][0] < key) and (key < self.p[i+1][0]) :
                        self.p.insert(i+1, [key, value])
       
        if self.is_full() :
            self.split()


    def split(self): #leaf나 nonLeaf 모두 일어날수 있음

        mid = self.m // 2
        right = Node(self.m)
        right.r = self.r
        right.parent= self.parent

        if self.parent is None :
            parentNode = Node(self.m)
            self.parent = parentNode
            right.parent = parentNode
            parentNode.p.append([self.p[mid][0], self])
            parentNode.r = right
            parentNode.leaf = False

        else :
            key = self.p[mid][0]
            if key < self.parent.p[0][0] :
                self.parent.p.insert(0, [key, self])
                self.parent.p[1][1] = right
            elif key > self.parent.p[len(self.parent.p)-1][0] :
                self.parent.p.insert(len(self.parent.p), [key, self])
                self.parent.r = right
            else :
                for i in range(0, len(self.parent.p)-1) :
                    if (self.parent.p[i][0] < key) and (key < self.parent.p[i+1][0]) :
                        self.parent.p.insert(i+1, [key, self])
                        self.parent.p[i+2][1] = right

        if self.r is not None and self.leaf is False :
            self.r.parent = right
        self.r = self.p[mid][1]

        if self.leaf is False :
            right.leaf = False
            self.p.pop(mid)
            for i in range(mid, len(self.p)) :
                self.p[mid][1].parent = right
                right.p.append(self.p.pop(mid))
        else :
            for i in range(mid, len(self.p)) :
                right.p.append(self.p.pop(mid))
            self.r = right

        if self.parent.is_full() :
            self.parent.split()
                  


    def show(self):
        if self.leaf is False : #NonLeaf Node
            for i in range(0, len(self.p)) :
                print(self.p[i][0], end = ' ')
            print()
        else : #Leaf Node
            for i in range(0, len(self.p)) :
                print(self.p[i][0], self.p[i][1])

    def is_underflow(self) :
        if len(self.p) == (self.m-1) // 2 - 1 :
            return True

        return False

    def sibling_underflow(self) :
        if len(self.p) == (self.m-1) // 2 :
            return True

        return False

    def index_of_the_node(self) :
        for i in range(0, len(self.parent.p)) :
            if self.parent.p[i][1] == self :
                return i
        return False #self.r is pointing the node

    def which_sibling(self) :
        index = self.index_of_the_node()
        if type(index) is int :
            if index == 0 : #leftmost node
                if len(self.parent.p) == 1 : #case of (m == 3)
                    if self.parent.r.sibling_underflow() is False :
                        return self.parent.r, False
                    else :
                        return False, self.parent.r
                else :
                    if self.parent.p[index + 1][1].sibling_underflow() is False :
                        return self.parent.p[index + 1][1], False
                    else :
                        return False, self.parent.p[index + 1][1]

            
            elif index == len(self.parent.p) - 1 : #special case
                if self.parent.p[index - 1][1].sibling_underflow() is False :
                    return self.parent.p[index - 1][1], True
                elif self.parent.r.sibling_underflow() is False :
                    return self.parent.r, False
                elif self.parent.p[index - 1][1].sibling_underflow() is True :
                    return True, self.parent.p[index - 1][1]
                else :
                    return False, self.parent.r

            else :
                if index > 0  and self.parent.p[index - 1][1].sibling_underflow() is False :
                    return self.parent.p[index - 1][1], True #borrow from left sibling

                elif index < len(self.parent.p)-1 and self.parent.p[index + 1][1].sibling_underflow() is False :
                    return self.parent.p[index + 1][1], False #borrow from right sibling
            
                elif index > 0  and self.parent.p[index - 1][1].sibling_underflow() is True :
                    return True, self.parent.p[index - 1][1] #flag to merge with left node

                elif index < len(self.parent.p)-1 and self.parent.p[index + 1][1].sibling_underflow() is True :
                    return False, self.parent.p[index + 1][1] #flag to merge with right node


        else : #rightmost node
            if self.parent.p[len(self.parent.p)-1][1].sibling_underflow() is False :
                return self.parent.p[len(self.parent.p)-1][1], True
            else :
                return True, self.parent.p[len(self.parent.p)-1][1]


    def borrow(self, tuple) :
        index = self.index_of_the_node()
        if tuple[1] == True : #left borrow
            left = tuple[0]
            if self.leaf is True :
                temp = left.p.pop(len(left.p)-1)
                self.p.insert(0, temp)
                if index is False :
                    self.parent.p[len(self.parent.p)-1][0] = temp[0]
                else :
                    self.parent.p[index-1][0] = temp[0]
            else :
                length = len(left.p)
                if index is False :
                    self.p.insert(0,[self.parent.p[len(self.parent.p)-1][0], left.r])
                    self.parent.p[len(self.parent.p)-1][0] = left.p[length-1][0]
                else :
                    self.p.insert(0,[self.parent.p[index][0], left.r])
                    self.parent.p[index][0] = left.p[length-1][0]
                left.r = left.p[length-1][1]
                left.p.pop(length-1)

        else : #right borrow
            right = tuple[0]
            if self.leaf is True :
                temp = right.p.pop(0)
                self.p.append(temp)
                self.parent.p[index][0] = right.p[0][0]
            else :
                self.p.append([self.parent.p[index][0], self.r])
                self.parent.p[index][0] = right.p[0][0]
                self.r = right.p[0][1]
                self.r.parent = self
                right.p.pop(0)

    def merge(self, tuple) :
        index = self.index_of_the_node()

        if tuple[0] == True : #merge with left node
            left = tuple[1]
            if self.leaf is True :
                self.p = left.p + self.p
                if index is False : #if parent.r is pointing self node
                    self.parent.p.pop(len(self.parent.p)-1)
                    if len(self.parent.p) > 0 :
                        self.parent.p[len(self.parent.p)-1][1].r = self
                else :
                    if index > 1 :
                        self.parent.p[index-2][1].r = self
                    self.parent.p.pop(index - 1)
                    
                del left
 
                
            else :
                if index is False :
                    self.p.insert(0, [self.parent.p[len(self.parent.p)-1][0], left.r])
                else :
                    self.p.insert(0,[self.parent.p[index-1][0], left.r])

                self.p = left.p + self.p

                if index is False : #if parent.r is pointing self node
                    self.parent.p.pop(len(self.parent.p)-1)
                else :
                    self.parent.p.pop(index - 1)
                del left
        else : #merge with right node
            right = tuple[1]

            if self.leaf is True :
                self.p = self.p + right.p
                self.r = right.r
                if index + 1 == len(self.parent.p) : #special case
                    self.parent.r = self
                else :
                    self.parent.p[index+1][1] = self
                self.parent.p.pop(index)
                del right
            else :
                self.p.append([self.parent.p[index][0], self.r])
                self.p = self.p + right.p
                if index + 1 == len(self.parent.p) :
                    self.parent.r = self
                else :
                    self.parent.p[index+1][1] = self
                self.parent.p.pop(index)
                del right



        



class BplusTree(object) :
    '''

    '''
    def __init__(self, m) :
        self.root = Node(m)
       
    def insert(self, key, some) :
        flag = self.find_node(self.root, key)
        if flag is None :
            self.root.add(key, some)
        else :
            flag.add(key, some)
            if self.root.parent is not None :
                self.root = self.root.parent


    def delete(self, key) :
        flag = self.find_node(self.root, key)
        index = -1
        for i in range(0, len(flag.p)) :
            if key == flag.p[i][0] :
                index = i
                break
        if index == -1 : #if no key
            print("There is no such a key in this tree")
            return

        '''
        delete
        '''
        if flag.sibling_underflow() is False :
            flag.p.pop(index)
            if index == 0 and flag.index_of_the_node() > 0:
                flag.parent.p[flag.index_of_the_node()-1][0] = flag.p[0][0]
        else :
            flag.p.pop(index)
            while True :
                if flag.parent is None :#if flag is root
                    self.root = self.root.r
                    break

                tuple = flag.which_sibling()

                if type(tuple[0]) is bool : #merge
                    flag.merge(tuple)
                else : #borrow
                    flag.borrow(tuple)

                if flag.parent.is_underflow() is True :
                    flag = flag.parent
                else :
                    break
            

    def find(self, node, key) :
        '''
        Return location of the Node having the key
        '''
        if node.leaf is True and len(node.p) == 0 : # First Input Case
            return None

        elif node.leaf is True : # if Leaf Node
            return node

        else : # if NonLeaf and Not Root Node
            node.show()
            if key < node.p[0][0] :
                return self.find(node.p[0][1], key) 
            elif key >= node.p[len(node.p) - 1][0] :
                return self.find(node.r, key)
            else :
               for i in range(0, len(node.p) - 1) :
                   if (node.p[i][0] <= key) and (key < node.p[i+1][0]) is True :
                       return self.find(node.p[i+1][1], key)

    def find_node(self, node, key) :
        '''
        Return location of the Node having the key
        '''
        if node.leaf is True and len(node.p) == 0 : # First Input Case
            return None

        elif node.leaf is True : # if Leaf Node
            return node

        else : # if NonLeaf and Not Root Node
            if key < node.p[0][0] :
                return self.find_node(node.p[0][1], key) 
            elif key >= node.p[len(node.p) - 1][0] :
                return self.find_node(node.r, key)
            else :
               for i in range(0, len(node.p) - 1) :
                   if (node.p[i][0] <= key) and (key < node.p[i+1][0]) is True :
                       return self.find_node(node.p[i+1][1], key)
    

    def search(self, key) :
        temp = self.find(self.root, key)
        
        for i in range(0, len(temp.p)) :
            if temp.p[i][0] == key :
                print(key,', ', temp.p[i][1])
                return
        print('NOT FOUND')
        return

    def range_search(self, key1, key2) :
        '''
        key1 < key2
        '''
        
        node1 = self.find_node(self.root, key1)
        node2 = self.find_node(self.root, key2)
        temp = node1.r
        flag = False

        for i in range(0, len(node1.p)) :
            if flag :
                print(node1.p[i][0],', ', node1.p[i][1])
            elif node1.p[i][0] >= key1 :
                flag = True
                print(node1.p[i][0],', ', node1.p[i][1])

        while temp != node2 :
            temp.show()
            temp = temp.r
            if temp == None :
                return

        for i in range(0, len(node2.p)) :
            if node2.p[i][0] > key2 :
                flag = False
                break
            elif flag :
                print(node2.p[i][0],', ', node2.p[i][1])
               
            

    def in_this_tree(self, key) :
        temp = self.find_node(self.root, key)
        if temp == None : #tree is empty
            return False
        else:
            for i in range(0, len(temp.p)) :
                if temp.p[i][0] == key :
                    return True
            return False

    def show_all(self, node) : # DFS
        node.show()
        if node.leaf is False :
            for i in range(0, len(node.p)) :
                if type(node.p[i][1]) is Node :
                    self.show_all(node.p[i][1])
            if type(node.r) is Node :
                self.show_all(node.r)


if __name__ == '__main__' :
    if sys.argv[1] == '-c' :
        with open(sys.argv[2],mode='wb') as f:
            Tree = BplusTree(int(sys.argv[3]))
            pickle.dump(Tree,f)
    elif sys.argv[1] == '-i' :
        with open(sys.argv[2],mode='r+b') as f :
            bptree=pickle.load(f)
        with open(sys.argv[2],mode='wb') as f :
            with open(sys.argv[3],mode='r') as insertFile :
                csv_reader = csv.reader(insertFile,delimiter=',')
                for row in csv_reader :
                    bptree.insert(int(row[0]),int(row[1]))
            pickle.dump(bptree,f)
    elif sys.argv[1] == '-d' :
        with open(sys.argv[2],mode='r+b') as f :
            bptree=pickle.load(f)
        with open(sys.argv[2],mode='wb') as f:
            with open(sys.argv[3],mode='r') as deleteFile :
                csv_reader = csv.reader(deleteFile,delimiter=',')
                for row in csv_reader :
                    bptree.delete(int(row[0]))
            pickle.dump(bptree,f)
    elif sys.argv[1] == '-s' :
        with open(sys.argv[2],mode='rb') as f :
            bptree=pickle.load(f)
            key=int(sys.argv[3])
            bptree.search(key)
    elif sys.argv[1] == '-r' :
        with open(sys.argv[2],mode='rb') as f:
            bptree=pickle.load(f)
            bptree.range_search(int(sys.argv[3]),int(sys.argv[4]))