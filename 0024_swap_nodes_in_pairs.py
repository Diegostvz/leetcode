"""
LeetCode 24 - Swap Nodes in Pairs (Medium)

Problem: Given a linked list, swap every two adjacent nodes and return its head. Solve it
without modifying the values in the nodes (only the nodes themselves may be changed).
(0 <= number of nodes <= 100, 0 <= Node.val <= 100)

Approach 1 - Dummy node + relink each pair (swapPairs):
    Key idea: keep prev on the node BEFORE the current pair (a dummy at the start). While
    there are two nodes after prev, name everything needed BEFORE touching any arrow:
    first = prev.next, second = first.next, next_pair = second.next. Then relink three arrows:

        before: prev -> first -> second -> next_pair
        after:  prev -> second -> first -> next_pair

    first is now the last node of the swapped pair, so it becomes prev for the next pair.
    An odd last node is left untouched: the loop stops, and it is already linked to the
    previous pair through first.next = next_pair.

    Complexity (L = number of nodes):
        Time:  O(L) -> L // 2 iterations with O(1) work each.
        Space: O(1) -> only the dummy and a few pointers; nodes are relinked in place.

    Note:
        - Changing an arrow loses what it pointed to: save next_pair BEFORE second.next = first,
          or the rest of the list is unreachable.
        - All three arrows must change. Forgetting first.next = next_pair leaves 1 -> 2 while
          2 -> 1, creating a cycle (to_list would never end).
        - No need to count the nodes: `while prev.next and prev.next.next` handles an odd
          length by itself.
        - Recursive alternative: swap the first pair and point first to swapPairs(next_pair).
          Same time, but O(L) space for the call stack.
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
    def swapPairs(self, head: ListNode | None) -> ListNode | None:
        """Relink every pair of adjacent nodes: prev -> 1 -> 2 -> 3 becomes prev -> 2 -> 1 -> 3."""
        dummy = ListNode(0, head)
        prev = dummy  # node before the current pair

        while prev.next and prev.next.next:  # at least two nodes left to swap
            first = prev.next
            second = first.next
            next_pair = second.next  # save it BEFORE changing any arrow

            prev.next = second  # prev -> 2
            second.next = first  # 2 -> 1
            first.next = next_pair  # 1 -> 3
            prev = first  # 1 is the last node of the swapped pair

        return dummy.next


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 2, 3, 4], [2, 1, 4, 3]),
        ([], []),  # empty
        ([1], [1]),  # single node
        ([1, 2], [2, 1]),  # a single pair
        ([1, 2, 3], [2, 1, 3]),  # odd: last one stays
        ([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]),  # odd, longer
        ([7, 7, 7, 7], [7, 7, 7, 7]),  # equal values
        (
            list(range(1, 101)),
            [i + 1 if i % 2 else i - 1 for i in range(1, 101)],
        ),  # max size
    ]

    for values, expected in test_cases:
        result = to_list(sol.swapPairs(build_list(values)))
        assert result == expected, (values, result)

    # Swapping twice must give back the original list (and the same nodes)
    head = build_list([1, 2, 3, 4, 5])
    original_nodes = []
    node = head
    while node:
        original_nodes.append(node)
        node = node.next
    twice = sol.swapPairs(sol.swapPairs(head))
    node, i = twice, 0
    while node:
        assert node is original_nodes[i], "nodes must be relinked, not recreated"
        node, i = node.next, i + 1
    assert i == len(original_nodes)

    print("OK")
