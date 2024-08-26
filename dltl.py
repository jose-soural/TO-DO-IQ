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

    def detach_node(self, node):
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

    def insert_node_ab(self, node_a, node_b):
        """Inserts node_a in front of node_b."""
        node_a.next = node_b
        if node_b.prev is None:     # b was the head
            self.head = node_a
        else:
            node_b.prev.next = node_a
        node_a.prev = node_b.prev
        node_b.prev = node_a

        self._add_node_to_glossary(node_a)

    def move_node(self, node, new_position):
        """Moves a task node to the specified position in the DLTL."""
        if new_position < 1 or new_position > self.size:
            print("Error: Invalid position.")
            return None

        self.detach_node(node)
        self.insert_node(node, new_position)

    def move_node_ab(self, node_a, node_b):
        """Moves node_a in front of node_b."""
        self.detach_node(node_a)
        self.insert_node_ab(node_a, node_b)

    def rename_node(self, node, new_name):
        """Renames the given task node and updates the glossary."""
        self._remove_node_from_glossary(node)
        node.name = new_name
        self._add_node_to_glossary(node)

    @staticmethod
    def change_description(node, new_description):
        """Changes the description of the given task node."""
        node.description = new_description

    @staticmethod
    def change_status(node, new_status):
        """Changes the status of the given task node."""
        node.status = new_status

    def display_task_names(self):
        """Displays the names of all tasks as a numbered list and returns
        a list of pointers to the numbered tasks."""

        current = self.head
        result = [None]*self.size
        for i in range(self.size):
            print(f'{i+1})   {current.name}')
            result[i] = current
            i += 1
            current = current.next
        return result

    def display_task_names_conditional(self, status):
        """Displays the names of tasks of the given status as a numbered list and returns
        a list of pointers to the numbered tasks."""
        current = self.head
        result = []
        i = 1
        for _ in range(self.size):
            if current.status == status:
                print(f'{i})   {current.name}')
                result.append(current)
                i += 1
            current = current.next
        return result


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
        if self.head is not None:
            self.head.prev = None
        waker.next = None

        self._remove_node_from_glossary(waker)
        return waker

    def wake_up_sleepers(self, end_date, target_dltl):
        """Wakes up all sleepers whose wake-up ('until') date is before the end_date (included)
        and appends them to the target DLTL."""
        while self.head is not None and self.head.until <= end_date:
            target_dltl.append_node(self.wake_up_head())
        if self.head is None:   # The list emptied completely
            self.tail = None

    @staticmethod
    def change_frequency(node, new_frequency):
        """Changes the frequency of the given task node."""
        node.frequency = new_frequency

    def display_task_names(self):
        """Displays the names AND wake-up ('until') date of all tasks as a numbered list
        and a list of pointers to the numbered tasks."""
        current = self.head
        result = [None] * self.size
        for i in range(self.size):
            print(f'{i+1})   {current.name}   awakens in {(current.until-today).days} days, on {current.until}.')
            result[i] = current
            i += 1
            current = current.next
        return result


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
        self.parent.size += 1
        self.size += 1

    def _remove_node_from_glossary(self, node):
        """A helper function. For member DLTLs, it removes the key:node from the parent's glossary."""
        del self.parent.glossary[node.name]
        self.parent.size -= 1
        self.size -= 1

    def fetch_node(self, name):
        """A helper function. For member DLTLs, it fetches the node by its name from the parent's glossary."""
        node = self.parent.glossary.get(name)
        if node is None:
            print("Error: Task not found.")     # Potentially want an error instead.
        return node

    def display_task_names(self, target_list, initial_index=1):
        """Displays the names of all tasks as a numbered list (starting from a given list index) and alters the
        given list in the corresponding manner. Returns the changed list AND the last displayed index + 1."""

        current = self.head
        for _ in range(self.size):
            print(f'{initial_index})   {current.name}')
            target_list[initial_index-1] = current
            initial_index += 1
            current = current.next
        return target_list, initial_index


class DLTLGroup:
    """A group of DLTLs with a common glossary."""

    def __init__(self):
        self.members = {}
        self.glossary = {}
        self.ordering = []
        self.size = 0

    def initiate_member(self, member_name, ordering_key: dict):
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
        member = self.members.pop(member_name)
        if member is None:
            return None         # Do I want to raise an error? Or to say something?

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

    def append_node(self, node, ordering_key: dict):
        """Appends the node to the appropriate member of the group (if said member doesn't exist, it creates it)"""
        if (freq := node.frequency) not in self.members:
            self.initiate_member(freq, ordering_key)
        self.members[freq].append_node(node)

    def _detach_node(self, node):
        """Detaches a node from the DLTL group."""
        freq = node.frequency
        member = self.members[freq]
        member.detach_node(node)

        if member.size == 0:
            del self.members[freq]
            self.ordering.remove(freq)

    def move_across_group(self, node, new_dltl, ordering_key: dict):
        """Moves the given node to the specified DLTL in the group (which it creates if necessary)."""
        self._detach_node(node)
        node.frequency = new_dltl
        self.append_node(node, ordering_key)

    def display_task_names(self):
        """Displays the names of all tasks (in the group) as a numbered list
        and returns a list of pointers to the numbered tasks."""

        result = [None] * self.size
        initial_index = 1
        for frequency in self.ordering:
            print(frequency, ":", sep="")
            result, initial_index = self.members[frequency].display_task_names(result, initial_index)
            print()
        return result

    def count_to_member(self, node_position, search_reversed=False):
        """Finds the member DLTL which contains the node of the given position in the group and its position in it."""
        if search_reversed:      # Searching from the back
            i = -1
            current = self.members[self.ordering[-i]]
            while node_position > current.size:
                node_position -= current.size
                i -= 1
                current = self.members[self.ordering[i]]
            node_position = current.size - node_position + 1        # Converting back to position from the start
        else:
            i = 0
            current = self.members[self.ordering[i]]
            while node_position > current.size:
                node_position -= current.size
                i += 1
                current = self.members[self.ordering[i]]
        return current, node_position

    def fetch_node_at_position(self, position):
        if position < 1 or position > (size := self.size):
            print("Error: Invalid position.")
            return None
        if position > size // 2:  # Closer to the end
            member, node_position = self.count_to_member(size - position + 1, True)
        else:
            member, node_position = self.count_to_member(position)
        return member.fetch_node_at_position(node_position)

    def moving_across_group_warning(self):
        user_input = input("Warning: You are attempting to move a task to a list with a different frequency."
                           "Do you wish to proceed? ('Y'/'N')")
        if user_input == "N":
            print("Canceling move request.")
            return user_input
        elif user_input == "Y":
            return user_input
        else:
            print("Did not understand response. Please try again.")
            return self.moving_across_group_warning()

    def move_node_ab(self, node_a, node_b):
        if (freq_a := node_a.frequency) == (freq_b := node_b.frequency):
            self.members[freq_a].move_node_ab(node_a, node_b)
            return "N", "N"  # So it doesn't throw an error
        elif self.moving_across_group_warning() == "N":
            return "N", "N"             # So it doesn't throw an error
        else:
            self._detach_node(node_a)
            node_a.frequency = freq_b
            self.members[freq_b].insert_task_ab(node_a, node_b)
            return freq_a, node_a       # This is for reflecting the change in the outer DLTL as well

    def move_node(self, node, new_position):
        node_b = self.fetch_node_at_position(new_position)
        if node_b is None:
            return None
        return self.move_node_ab(node, node_b)

    def change_frequency(self, node, new_frequency, ordering_key: dict):
        self._detach_node(node)
        node.frequency = new_frequency
        self.append_node(node, ordering_key)

    def rename_node(self, node, new_name):
        """Renames the given task node and updates the glossary."""
        self.members[node.frequency].rename_node(node, new_name)

    @staticmethod
    def change_description(node, new_description):
        """Changes the description of the given task node."""
        node.description = new_description
