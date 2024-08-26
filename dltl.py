from datetime import date
today = date.today()


class TaskNode:
    """A node of a doubly linked list."""

    def __init__(self, name, frequency="once", description="", status="due", until=None):
        self.name = name
        self.frequency = frequency
        self.description = description
        self.status = status
        self.until = until
        self.prev = None
        self.next = None


class DLTL:
    """A doubly linked task list."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.glossary = {}
        self.size = 0

    def _add_node_to_glossary(self, node):
        """A helper function. For regular DLTLs, it adds the key:node pair their own glossary."""
        self.glossary[node.name] = node
        self.size += 1


    def _remove_node_from_glossary(self, node):
        """A helper function. For regular DLTLs, it removes the key:node from their own glossary."""
        del self.glossary[node.name]
        self.size -= 1

    def fetch_node(self, name):
        """A helper function. For regular DLTLs, it fetches the node by its name from the DLTL's own glossary."""
        node = self.glossary.get(name)
        if node is None:
            print("Error: Task not found.")     # Potentially want an error instead.
        return node

    def append_node(self, node):
        """Appends a node to the end of the DLTL."""
        if self.size == 0:  # If list is empty
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

        self._add_node_to_glossary(node)

    def _detach_node(self, node):
        """Detaches a node from the DLTL by the name of its task."""
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

        self._remove_node_from_glossary(node)

    def _detach_node_by_name(self, name):
        """Detaches a node from the DLTL by the name of its task."""
        node = self.fetch_node(name)
        if node is None:
            return None
        self._detach_node(node)

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

    def remove_position(self, position):
        """Remove a task node at the given position."""
        node = self.fetch_node_at_position(position)
        if node is None:
            return None
        self._detach_node(node)

    def insert_node(self, node, position):
        """Inserts a node to the specified position."""
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

        self._add_node_to_glossary(node)

    def move_task(self, name, new_position):
        """Moves a task (node) to the specified position."""
        node = self.fetch_node(name)
        if node is None:
            return None
        if new_position < 1 or new_position > self.size:
            print("Error: Invalid position.")
            return None

        self._detach_node(node)
        self.insert_node(node, new_position)

    def display_task_names(self, initial_index=1):
        """Displays the names of all tasks as a numbered list (starting from an arbitrary number) and returns the last index +1."""
        current = self.head
        for _ in range(self.size):
            print(f'{initial_index})   {current.name}')
            initial_index += 1
            current = current.next
        return initial_index

    def display_task_names_conditional(self, status, initial_index=1):
        """Displays the names of tasks of the given status as a numbered list (starting from an arbitrary number) and returns the last index +1."""
        current = self.head
        for _ in range(self.size):
            if current.status == status:
                print(f'{initial_index})   {current.name}')
                initial_index += 1
            current = current.next
        return initial_index


class SleeperDLTL(DLTL):
    """A DLTL specialized for sleeping tasks."""

    def add_sleeper(self, node):
        """Adds a sleeping task to the appropriate position in the DLTL, based on its wake-up ('until') date."""
        until = node.until

        successor = self.head
        while successor is not None and until > successor.until:
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

        self._add_node_to_glossary(node)

    def wake_up_head(self):
        """Wakes up the head of the DLTL (removes the node and passes it to the caller)."""
        waker = self.head
        if waker is None:
            return None     # This should never trigger
        self.head = self.head.next
        self.head.prev = None
        waker.next = None

        self._remove_node_from_glossary(waker)
        return waker

    def wake_up_sleepers(self, end_date, target_dltl):
        """Wakes up all sleepers whose wake-up ('until') date is before the end_date (included) and appends them to the target DLTL."""
        while self.head is not None and self.head.until <= end_date:
            target_dltl.append_node(self.wake_up_head())
        if self.head is None:   # The list emptied completely
            self.tail = None

    def display_task_names(self, initial_index=1):
        """Displays the names AND wake-up ('until') date of all tasks as a numbered list (starting from an arbitrary number) and returns the last index +1."""
        current = self.head
        for _ in range(self.size):
            print(f'{initial_index})   {current.name}   awakens in {(current.until-today).days()} days, on {current.until}.')
            initial_index += 1
            current = current.next
        return initial_index

class MemberDLTL(DLTL):
    """A DLTL that is part of a group of DLTLs (with a shared glossary)."""

    def __init__(self, parent_group):
        self.parent = parent_group
        self.head = None
        self.tail = None
        self.size = 0

    def _add_node_to_glossary(self, node):
        """A helper function. For member DLTLs, it adds the key:node pair to the parent's glossary."""
        self.parent.glossary[node.name] = node
        self.size += 1


    def _remove_node_from_glossary(self, node):
        """A helper function. For member DLTLs, it removes the key:node from the parent's glossary."""
        del self.parent.glossary[node.name]
        self.size -= 1

    def fetch_node(self, name):
        """A helper function. For member DLTLs, it fetches the node by its name from the parent's glossary."""
        node = self.parent.glossary.get(name)
        if node is None:
            print("Error: Task not found.")     # Potentially want an error instead.
        return node



class DLTLGroup():
    """A group of DLTLs with a common glossary."""

    def __init__(self):
        self.members = {}
        self.glossary = {}
        self.ordering = []

    def initiate_member(self, member_name, ordering_key:dict):
        """Creates an empty member DLTL of the given name and adds it to the group, to the appropriate position."""
        self.members[member_name] = MemberDLTL(self)

        # Add the member to the ordering. The search could be optimized, but that wouldn't change O(n) complexity.
        self.ordering.append(member_name)
        i = 0
        while ordering_key[self.ordering[i]] < ordering_key[member_name]:
            i += 1
        self.ordering.insert(i, member_name)
        self.ordering.pop()

    def remove_member(self, member_name):
        """Removes the specified DLTL from the group."""
        member = self.members.get(member_name)
        if member is None:
            return None         # Do I want to raise an error? Or to say something?

        del self.members[member_name]
        self.ordering.remove(member_name)

        # remove all deleted tasks from the glossary
        current = member.head
        for _ in range(member.size):
            del self.glossary[current.name]
            current = current.next

    def fetch_node(self, name):
        """A helper function. For regular DLTLs, it fetches the node by its name from the DLTL's own glossary."""
        node = self.glossary.get(name)
        if node is None:
            print("Error: Task not found.")     # Potentially want an error instead.
        return node

    def append_node(self, node, ordering_key:dict):
        """Appends the node to the appropriate member of the group (if said member doesn't exist, it creates it)"""
        if (freq := node.frequency) not in self.members:
            self.initiate_member(freq, ordering_key)
        self.members[freq].append_node(node)

    def _detach_node(self, name):
        """Detaches a node from the DLTL group by the name of its task."""
        node = self.fetch_node(name)
        if node is None:
            return None

        self.members[node.frequency]._detach_node(node)
        # a tady když to byl poslední, tak smazat member

    def _remove_from_special(task, collection):  # This could cause a meltdown
        """Not meant for the end user. Removes a task (and the corresponding DLTL) from the collection."""
        collection["glossary"].pop(task["name"], None)
        freq = task["frequency"]
        temp = collection["frequencies"][freq]
        temp.detach_node_by_name(task["name"])
        if temp.size == 0:
            del collection["frequencies"][freq]
            collection["ordering"].remove(freq)