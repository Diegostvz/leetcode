"""
LeetCode 21 - Merge Two Sorted Lists (Easy)

Problem: Given the heads of two sorted linked lists list1 and list2, merge them into one
sorted list by splicing together the nodes of the two lists, and return its head.
(0 <= number of nodes in each list <= 50, -100 <= Node.val <= 100)

Approach 1 - Dummy node + tail pointer (mergeTwoLists):
    Key idea: keep a dummy node in front of the result and a tail pointer to its last node.
    While both lists have nodes, attach the smaller head to tail, advance that list and
    advance tail. When one list runs out, attach the rest of the other one in a single step:
    it is already sorted and linked. Return dummy.next.
    The dummy removes the special case of choosing the first node: it is just one more
    iteration of the loop. It also handles empty inputs for free.

    Complexity (L1, L2 = lengths of the lists):
        Time:  O(L1 + L2) -> each iteration attaches one node; the leftover is attached in O(1).
        Space: O(1) -> no new nodes are created, existing nodes are relinked (only the dummy
               and a few pointers are extra).

    Note:
        - Optimal: the nodes must be compared to know their order, so O(L1 + L2) time is
          needed, and relinking in place uses no extra memory.
        - Moving a pointer (l1 = l1.next) vs changing an arrow (tail.next = l1): if there is a
          .next on the left of the =, the list changes; a bare variable only moves.
        - Attaching the leftover must happen AFTER the loop: if one list starts empty, the
          loop never runs.
        - Using <= instead of < keeps equal values in their original order (stable merge).
        - Recursive alternative: the smaller head points to the merge of the rest. Same time,
          but O(L1 + L2) space for the call stack.
        - This merge step is the core of merge sort on linked lists.
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
    def mergeTwoLists(
        self, list1: ListNode | None, list2: ListNode | None
    ) -> ListNode | None:
        """Attach the smaller head to the tail of the result, then the leftover."""
        dummy = ListNode()  # placeholder in front of the merged list
        tail = dummy  # last node of the merged list

        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        tail.next = list1 or list2  # attach whatever is left (already sorted)
        return dummy.next


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),  # both empty
        ([], [0], [0]),  # first empty
        ([0], [], [0]),  # second empty
        ([5], [1, 2, 3], [1, 2, 3, 5]),  # second list ends first
        ([1, 2, 3], [5], [1, 2, 3, 5]),  # first list ends first
        ([1, 1, 1], [1, 1], [1, 1, 1, 1, 1]),  # all equal
        ([-3, 0, 7], [-5, 2, 8, 9], [-5, -3, 0, 2, 7, 8, 9]),
        (list(range(0, 100, 2)), list(range(1, 100, 2)), list(range(100))),  # max size
    ]

    for values1, values2, expected in test_cases:
        result = to_list(sol.mergeTwoLists(build_list(values1), build_list(values2)))
        assert result == expected, (values1, values2, result)
    print("OK")
