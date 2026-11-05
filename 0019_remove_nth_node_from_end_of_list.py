"""
LeetCode 19 - Remove Nth Node From End of List (Medium)

Problem: Given the head of a linked list, remove the n-th node from the end of the list and
return its head. (1 <= sz <= 30 nodes, 0 <= Node.val <= 100, 1 <= n <= sz)
Follow up: could you do this in one pass?

Approach 1 - Two passes: count, then unlink (removeNthFromEnd):
    Key idea: to remove a node you must stand on the node BEFORE it and redirect its arrow:
    prev.next = prev.next.next. Going forward is the only way to move, so first count the
    nodes (length), then the node before the target is at length - n steps from a dummy
    node placed in front of head.
    The dummy guarantees that every real node has a previous one, even the head: removing
    the head (n == length) means 0 steps, i.e. unlinking dummy.next. Return dummy.next,
    which is the real head even if the original one was removed.

    Complexity (L = number of nodes):
        Time:  O(L) -> one full pass to count, plus at most L steps in the second pass.
        Space: O(1) -> only the dummy node and a few variables. The list itself is the
               input, so it does not count as extra space.

    Note:
        - Moving a pointer (current = current.next) does NOT change the list; only
          reassigning an arrow (node.next = ...) does.
        - next is an attribute, not a method: current.next(), with parentheses, raises
          TypeError: 'ListNode' object is not callable.
        - One-pass alternative (the follow up): two pointers, fast and slow, both starting
          at the dummy. Move fast n + 1 steps ahead, then move both together until fast is
          None: slow ends right before the node to remove. Same O(L) time and O(1) space,
          but a single traversal.
"""


class ListNode:
    """LeetCode provides this definition; needed here to run locally."""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values: list[int]) -> ListNode | None:
    """Build a linked list from a Python list (test helper)."""
    dummy = ListNode()
    current = dummy
    for v in values:
        current.next = ListNode(v)
        current = current.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    """Convert a linked list back to a Python list (test helper)."""
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


class Solution:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        """Count the nodes, then stop right before the target and unlink it."""
        dummy = ListNode(
            0, head
        )  # dummy node in front of head, so the head has a previous

        # First pass: count the nodes
        length = 0
        current = head
        while current:
            length += 1
            current = current.next

        # Second pass: stop at the node BEFORE the one to remove
        prev = dummy
        for _ in range(length - n):
            prev = prev.next
        prev.next = prev.next.next  # skip the target node

        return dummy.next


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5]),
        ([1], 1, []),  # remove the only node
        ([1, 2], 1, [1]),  # remove the last node
        ([1, 2], 2, [2]),  # remove the head -> needs the dummy
        ([0, 1, 2], 1, [0, 1]),
        ([1, 2, 3, 4, 5], 5, [2, 3, 4, 5]),  # head of a longer list
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4]),  # tail of a longer list
        (list(range(30)), 15, [v for v in range(30) if v != 15]),  # max size
    ]

    for values, n, expected in test_cases:
        result = to_list(sol.removeNthFromEnd(build_list(values), n))
        assert result == expected, (values, n, result)
    print("OK")
