class TaskNode:
    """A node of a doubly linked list"""

    def __init__(self, task):
        self.task = task
        self.name = task["name"]
        self.prev = None
        self.next = None


class DLTL:
    """A doubly linked task list"""

    def __init__(self):
        self.head = None
        self.tail = None
        self.glossary = {}
        self.size = 0

    def append_task(self, task):
        node = TaskNode(task)
        if self.size == 0:  # If list is empty
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

        self.glossary[task["name"]] = node
        self.size += 1

    def _remove_node(self, node):
        """Remove a node from the list."""
        if node.prev:
            node.prev.next = node.next
        else:  # Node is head
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:  # Node is tail
            self.tail = node.prev

        del self.glossary[node.name]
        self.size -= 1

    def remove_task(self, name):
        node = self.glossary.get(name, None)
        if node is None:
            print("Error: Task not found.")
            return -1
        self._remove_node(node)

    def fetch_task(self, name):
        """Fetch a task by its name."""
        node = self.glossary.get(name)
        if node is None:
            print("Error: Task not found.")
            return -1
        return node.task

    def fetch_node_at_position(self, position):
        """Fetch the node at the given position in the DLTL."""
        if position < 1 or position > (size := self.size):
            print("Error: Invalid position.")
            return -1
        if position > size // 2:  # Closer to the end
            current = self.tail
            for _ in range(size - position):
                current = current.prev
        else:  # Closer to the start
            current = self.head
            for _ in range(position - 1):
                current = current.next
        return current

    def remove_position(self, position: int) -> None:
        """Remove a task at a specific position."""
        node = self.fetch_node_at_position(position)
        self._remove_node(node)

    def move_task(self, name, new_position):
        node = self.glossary.get(name)
        if node is None:
            print("Error: Task not found.")
            return -1
        if new_position < 1 or new_position > self.size:
            print("Error: Invalid position.")
            return -1

        self._remove_node(node)

        # Insert at the new position
        if new_position == 1:
            node.next = self.head
            node.prev = None
            if self.head:
                self.head.prev = node
            self.head = node
            if self.size == 0:
                self.tail = node
        else:
            predecessor = self.fetch_node_at_position(new_position - 1)
            node.next = predecessor.next
            node.prev = predecessor
            predecessor.next = node
            if node.next:
                node.next.prev = node
            else:
                self.tail = node
        self.size += 1

    def display_tasks(self, initial_index=1):
        current = self.head
        for i in range(self.size):
            print(f'{initial_index+i})   {current.name}')
            current = current.next

class DLTLSquared(DLTL):
    """A doubly linked list of doubly linked task lists"""

