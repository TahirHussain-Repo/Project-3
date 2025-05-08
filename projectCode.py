# project3.py - CS4348 Project 3
import os
import struct
import csv
import sys

BLOCK_SIZE = 512
MAGIC = b'4348PRJ3'
T = 10
MAX_KEYS = 2 * T - 1
MAX_CHILDREN = 2 * T

class Header:
    def __init__(self, root=0, next_block=1):
        self.root = root
        self.next_block = next_block

    def to_bytes(self):
        return MAGIC + self.root.to_bytes(8, 'big') + self.next_block.to_bytes(8, 'big') + bytes(BLOCK_SIZE - 24)

    @staticmethod
    def from_bytes(data):
        if data[:8] != MAGIC:
            raise ValueError("Invalid index file format")
        root = int.from_bytes(data[8:16], 'big')
        next_block = int.from_bytes(data[16:24], 'big')
        return Header(root, next_block)

class BTreeNode:
    def __init__(self, block_id, parent=0, num_keys=0, keys=None, values=None, children=None):
        self.block_id = block_id
        self.parent = parent
        self.num_keys = num_keys
        self.keys = keys or [0] * MAX_KEYS
        self.values = values or [0] * MAX_KEYS
        self.children = children or [0] * MAX_CHILDREN

    def to_bytes(self):
        b = self.block_id.to_bytes(8, 'big')
        b += self.parent.to_bytes(8, 'big')
        b += self.num_keys.to_bytes(8, 'big')
        for k in self.keys: b += k.to_bytes(8, 'big')
        for v in self.values: b += v.to_bytes(8, 'big')
        for c in self.children: b += c.to_bytes(8, 'big')
        return b + bytes(BLOCK_SIZE - len(b))

    @staticmethod
    def from_bytes(data):
        block_id = int.from_bytes(data[0:8], 'big')
        parent = int.from_bytes(data[8:16], 'big')
        num_keys = int.from_bytes(data[16:24], 'big')
        keys = [int.from_bytes(data[24+i*8:32+i*8], 'big') for i in range(MAX_KEYS)]
        values = [int.from_bytes(data[176+i*8:184+i*8], 'big') for i in range(MAX_KEYS)]
        children = [int.from_bytes(data[328+i*8:336+i*8], 'big') for i in range(MAX_CHILDREN)]
        return BTreeNode(block_id, parent, num_keys, keys, values, children)

# File utilities
def read_header(f):
    f.seek(0)
    return Header.from_bytes(f.read(BLOCK_SIZE))

def write_header(f, header):
    f.seek(0)
    f.write(header.to_bytes())

def read_node(f, block_id):
    f.seek(block_id * BLOCK_SIZE)
    return BTreeNode.from_bytes(f.read(BLOCK_SIZE))

def write_node(f, node):
    f.seek(node.block_id * BLOCK_SIZE)
    f.write(node.to_bytes())

# B-tree operations
def insert(filename, key, value):
    with open(filename, 'r+b') as f:
        header = read_header(f)
        if header.root == 0:
            root = BTreeNode(header.next_block)
            root.num_keys = 1
            root.keys[0] = key
            root.values[0] = value
            header.root = root.block_id
            header.next_block += 1
            write_node(f, root)
            write_header(f, header)
        else:
            root = read_node(f, header.root)
            if root.num_keys == MAX_KEYS:
                new_root = BTreeNode(header.next_block)
                header.next_block += 1
                new_root.children[0] = root.block_id
                split_child(f, new_root, 0, root, header)
                insert_non_full(f, new_root, key, value, header)
                header.root = new_root.block_id
                write_node(f, new_root)
                write_header(f, header)
            else:
                insert_non_full(f, root, key, value, header)
                write_node(f, root)

def insert_non_full(f, node, key, value, header):
    i = node.num_keys - 1
    if node.children[0] == 0:
        while i >= 0 and key < node.keys[i]:
            node.keys[i + 1] = node.keys[i]
            node.values[i + 1] = node.values[i]
            i -= 1
        node.keys[i + 1] = key
        node.values[i + 1] = value
        node.num_keys += 1
        write_node(f, node)
    else:
        while i >= 0 and key < node.keys[i]:
            i -= 1
        i += 1
        child = read_node(f, node.children[i])
        if child.num_keys == MAX_KEYS:
            split_child(f, node, i, child, header)
            if key > node.keys[i]:
                i += 1
            child = read_node(f, node.children[i])
        insert_non_full(f, child, key, value, header)
        write_node(f, child)
        write_node(f, node)

def split_child(f, parent, index, child, header):
    new_child = BTreeNode(header.next_block, parent.block_id)
    header.next_block += 1
    new_child.num_keys = T - 1
    for j in range(T - 1):
        new_child.keys[j] = child.keys[j + T]
        new_child.values[j] = child.values[j + T]
    if child.children[0] != 0:
        for j in range(T):
            new_child.children[j] = child.children[j + T]
    child.num_keys = T - 1
    for j in range(parent.num_keys, index, -1):
        parent.children[j + 1] = parent.children[j]
        parent.keys[j] = parent.keys[j - 1]
        parent.values[j] = parent.values[j - 1]
    parent.children[index + 1] = new_child.block_id
    parent.keys[index] = child.keys[T - 1]
    parent.values[index] = child.values[T - 1]
    parent.num_keys += 1
    write_node(f, child)
    write_node(f, new_child)
    write_node(f, parent)
    write_header(f, header)

def search(f, block_id, key):
    node = read_node(f, block_id)
    i = 0
    while i < node.num_keys and key > node.keys[i]:
        i += 1
    if i < node.num_keys and key == node.keys[i]:
        print(f"Found: {key}, {node.values[i]}")
        return
    if node.children[0] == 0:
        print("Key not found.")
        return
    search(f, node.children[i], key)

def print_all(f, block_id):
    node = read_node(f, block_id)
    for i in range(node.num_keys):
        if node.children[i] != 0:
            print_all(f, node.children[i])
        print(f"{node.keys[i]} {node.values[i]}")
    if node.children[node.num_keys] != 0:
        print_all(f, node.children[node.num_keys])

def extract_all(f, block_id, writer):
    node = read_node(f, block_id)
    for i in range(node.num_keys):
        if node.children[i] != 0:
            extract_all(f, node.children[i], writer)
        writer.writerow([node.keys[i], node.values[i]])
    if node.children[node.num_keys] != 0:
        extract_all(f, node.children[node.num_keys], writer)

def load(filename, csvname):
    with open(csvname, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 2:
                continue
            insert(filename, int(row[0]), int(row[1]))

def main():
    if len(sys.argv) < 3:
        print("Usage: project3 <command> <args...>")
        return
    cmd = sys.argv[1]
    if cmd == 'create':
        if os.path.exists(sys.argv[2]):
            print("File already exists.")
            return
        with open(sys.argv[2], 'wb') as f:
            f.write(Header().to_bytes())
    elif cmd == 'insert':
        insert(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == 'search':
        with open(sys.argv[2], 'rb') as f:
            header = read_header(f)
            search(f, header.root, int(sys.argv[3]))
    elif cmd == 'print':
        with open(sys.argv[2], 'rb') as f:
            header = read_header(f)
            print_all(f, header.root)
    elif cmd == 'extract':
        if os.path.exists(sys.argv[3]):
            print("Output file already exists.")
            return
        with open(sys.argv[2], 'rb') as f, open(sys.argv[3], 'w', newline='') as out:
            header = read_header(f)
            writer = csv.writer(out)
            extract_all(f, header.root, writer)
    elif cmd == 'load':
        load(sys.argv[2], sys.argv[3])
    else:
        print("Unknown command.")

if __name__ == '__main__':
    main()
