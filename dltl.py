class Task_node:
    """A node of a doubly linked list"""

    def __init__(self, task, prev=None, next=None):
        self.task = task
        self.prev = prev
        self.next = next


class DLTL:
    """A doubly linked task list"""

    def __init__(self, head=None, tail=None):
        self.head = None
        self.tail = None