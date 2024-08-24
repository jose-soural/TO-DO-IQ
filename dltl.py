from datetime import date
today = date.today()


class TaskNode:
    """A node of a doubly linked list."""

    def __init__(self, task):
        self.task = task
        self.prev = None
        self.next = None


class DLTL:
    """A doubly linked task list."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.glossary = {}
        self.size = 0

    def append_node(self, node):
        """Appends a node to the end of the DLTL."""
        if self.size == 0:  # If list is empty
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

        self.glossary[node.task["name"]] = node
        self.size += 1

    def append_task(self, task):
        """Appends a task to the end of the DLTL."""
        self.append_node(TaskNode(task))

    def _remove_node(self, node):
        """Removes a node from the DLTL."""
        if node.prev is None:   # The node is the head
            self.head = node.next
        else:
            node.prev.next = node.next
            node.prev = None

        if node.next is None:      # The node is the tail
            self.tail = node.prev
        else:
            node.next.prev = node.prev
            node.next = None

        del self.glossary[node.task["name"]]
        self.size -= 1

    def remove_task(self, name):
        """Removes a task by its name."""
        node = self.glossary.get(name)
        if node is None:
            print("Error: Task not found.")
            return None                              # Potentially want an error instead.
        self._remove_node(node)

    def fetch_node(self, name):
        """Fetches a node by the name of its task."""
        node = self.glossary.get(name)
        if node is None:
            print("Error: Task not found.")
            return None
        return node

    def fetch_task(self, name):
        """Fetches a task by its name."""
        node = self.fetch_node(name)
        if node is None:
            return None
        return node.task

    def fetch_node_at_position(self, position):
        """Fetches the node at the given position in the DLTL."""
        if position < 1 or position > (size := self.size):
            print("Error: Invalid position.")
            return None
        if position > size // 2:  # Closer to the end
            current = self.tail
            for _ in range(size - position):
                current = current.prev
        else:  # Closer to the start
            current = self.head
            for _ in range(position - 1):
                current = current.next
        return current

    def fetch_task_at_position(self, position):
        """Fetches the task at the given position in the DLTL."""
        node = self.fetch_node_at_position(position)
        if node is None:
            return None
        return node.task

    def remove_position(self, position):
        """Remove a task (node) at the given position."""
        node = self.fetch_node_at_position(position)
        if node is None:
            return None
        self._remove_node(node)

    def insert_node(self, node, position):
        """Adds a node at the specified position."""
        if position < 1 or position > self.size:
            print("Error: Invalid position.")
            return None

        if position == 1:
            node.next = self.head
            if self.head is None:   # List was empty
                self.tail = node
            else:
                self.head.prev = node
            self.head = node

        else:
            predecessor = self.fetch_node_at_position(position - 1)
            node.next = predecessor.next
            node.prev = predecessor
            predecessor.next = node
            if node.next is None:
                self.tail = node
            else:
                node.next.prev = node

        self.glossary[node.task["name"]] = node
        self.size += 1

    def insert_task(self, task, position):
        """Adds a task at the specified position."""
        self.insert_node(TaskNode(task), position)

    def move_task(self, name, new_position):
        """Moves a task (node) to the specified position."""
        node = self.glossary.get(name)
        if node is None:
            print("Error: Task not found.")
            return None
        if new_position < 1 or new_position > self.size:
            print("Error: Invalid position.")
            return None

        self._remove_node(node)
        self.insert_node(node, new_position)

    def display_task_names(self, initial_index=1):
        """Displays the names of all tasks as a numbered list (starting from an arbitrary number) and returns the last index +1."""
        current = self.head
        for _ in range(self.size):
            print(f'{initial_index})   {current.task["name"]}')
            initial_index += 1
            current = current.next
        return initial_index

    def display_task_names_conditional(self, status, initial_index=1):
        """Displays the names of tasks of the given status as a numbered list (starting from an arbitrary number) and returns the last index +1."""
        current = self.head
        for _ in range(self.size):
            if current.task["status"] == status:
                print(f'{initial_index})   {current.task["name"]}')
                initial_index += 1
            current = current.next
        return initial_index


class SleeperDLTL(DLTL):
    """A DLTL specialized for sleeping tasks."""

    def add_sleeper(self, task):
        """Adds a sleeping task to the appropriate position in the DLTL, based on its wake-up ('until') date."""
        node = TaskNode(task)
        until = task["until"]

        successor = self.head
        while successor is not None and until > successor.task["until"]:
            successor = successor.next
        if successor is None:       # The added task goes at the end
            if self.tail is None:   # The list is empty
                self.head = self.tail = node
            else:
                self.tail.next = node
                node.prev = self.tail
                self.tail = node
        else:
            if successor == self.head:  # The added task goes at the start
                node.next = self.head
                self.head.prev = node
                self.head = node
            else:                       # The added task goes somewhere in the middle
                node.next = successor
                node.prev = successor.prev
                node.prev.next = node
                node.next.prev = node

        self.glossary[node.task["name"]] = node
        self.size += 1

    def wake_up_head(self):
        """Wakes up the head of the DLTL (removes the node and passes it to the caller)."""
        waker = self.head
        if waker is None:
            return None     # This should never trigger
        self.head = self.head.next
        self.head.prev = None
        waker.next = None

        del self.glossary[waker.task["name"]]
        self.size -= 1
        return waker

    def wake_up_sleepers(self, end_date, target_dltl):
        """Wakes up all sleepers whose wake-up ('until') date is before the end_date (included) and appends them to the target DLTL."""
        while self.head is not None and self.head.task["until"] <= end_date:
            target_dltl.append_node(self.wake_up_head())
        if self.head is None:   # The list emptied completely
            self.tail = None

    def display_task_names(self, initial_index=1):
        """Displays the names AND wake-up ('until') date of all tasks as a numbered list (starting from an arbitrary number) and returns the last index +1."""
        current = self.head
        for _ in range(self.size):
            print(f'{initial_index})   {current.task["name"]}   awakens in {(current.task["until"]-today).days} days, on {current.task["until"]}.')
            initial_index += 1
            current = current.next
        return initial_index
