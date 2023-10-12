import ast
from itertools import combinations

class FP_treeNode:
    def __init__(self, itemname, count, parrentNode):
        self.itemname = itemname
        self.count = count
        self.parrentNode = parrentNode
        self.nodeLink = None
        self.children = {}
        
    def increase(self, occurrences):
        self.count += occurrences
        
    def display(self, ind=0):
        print(f"{' '*ind} {self.itemname} {self.count}")
        for child in self.children.values():
            child.display(ind+1)
        
# Update header linklist
def update_Header(node, target_node):
    while node.nodeLink is not None:
        node = node.nodeLink
    node.nodeLink = target_node

def update_FPtree(items, now_Node, header_table, count):
    if items[0] in now_Node.children:
        # 判斷是否已存在於子結點，有的話子count+1
        now_Node.children[items[0]].increase(count)
    else:
        # 創建新的分支
        now_Node.children[items[0]] = FP_treeNode(items[0], count, now_Node)
        # 更新header linklist
        if header_table[items[0]][1] == None:
            header_table[items[0]][1] = now_Node.children[items[0]]
        else:
            update_Header(header_table[items[0]][1], now_Node.children[items[0]])
    
    # 遞迴往下
    if len(items) > 1:
        update_FPtree(items[1::], now_Node.children[items[0]], header_table, count)

def create_itemset_newdata(dataset, min_sup_num):
    l1 = {}
    for transaction in dataset:
        for item in transaction:
            if item not in l1:
                l1[item] = 1
            else:
                l1[item] += 1   
    delete_item = []
    for item, value in l1.items():
        if value < min_sup_num:
            delete_item.append(item)
    for delete in delete_item:
        del l1[delete]
        for tran in dataset:
            if delete in tran:
                tran.remove(delete)
    # 各項目線次數排序
    item_head = sorted(l1.items(), key=lambda x: x[1], reverse=True)
    # print(item_head)
    # [("['38']", 2265), ("['36']", 1879),...]
    new_dataset = []
    # transaction 內元素依照次數sort排序
    for transaction in dataset:
        new_data = []
        for item, value in item_head:
            # print(item, value)
            if item in transaction:
                new_data.append(item)
        new_dataset.append(new_data)
    # print(new_dataset)
    
    return new_dataset, item_head

# 回朔找prefix pattern
def ascendFPtree(leafNode, prefixPath):
    if leafNode.parrentNode != None:
        prefixPath.append(leafNode.itemname)

def do_fp_growth(dataset, min_sup_num):
    dataset = [['m','br','be'],
               ['br','c'],
               ['br','e'],
               ['m','br','c'],
               ['m','e'],
               ['br','e'],
               ['m','e'],
               ['m','br','e','be'],
               ['m','br','e']]
    min_sup_num = 2
    new_dataset, item_head = create_itemset_newdata(dataset, min_sup_num)
    
    header_table = {}
    for item in item_head:
        header_table[item[0]] = [item[1], None] # [count, node]
    FP_tree = FP_treeNode('Null Set', 1, None)
    for ordered_transaction in new_dataset:
        update_FPtree(ordered_transaction, FP_tree, header_table, 1)
    # FP_tree.display()
    return {}