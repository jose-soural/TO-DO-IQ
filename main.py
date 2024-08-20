class Task_node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    def move_to_front(self, node):
        if node == self.head:
            return
        self.remove(node)
        self.append(node)

    def display(self):
        current = self.head
        while current:
            print(f'({current.key}: {current.value})', end=' <-> ')
            current = current.next
        print('None')

class Cache:
    def __init__(self):
        self.cache = {}  # Dictionary to map keys to nodes
        self.order = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.order.move_to_front(node)
            return node.value
        return None

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.order.move_to_front(node)
        else:
            new_node = Task_node(key, value)
            self.order.append(new_node)
            self.cache[key] = new_node

    def display(self):
        self.order.display()

# Example usage
cache = Cache()
cache.put(1, 'A')
cache.put(2, 'B')
cache.put(3, 'C')
cache.display()  # Output: (3: C) <-> (2: B) <-> (1: A) <-> None

print(cache.get(2))  # Output: 'B'
cache.display()  # Output: (2: B) <-> (3: C) <-> (1: A) <-> None

# Create, delete, mark as done, set asleep, view details, rename, change frequency, change description
