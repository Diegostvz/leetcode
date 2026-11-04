"""
LeetCode 19 - Remove Nth Node From End Of List (Medium)

Problem:

Approach 1 -

    Complexity:
        Time:  O().
        Space: O()

    Note:

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

        dummy_head = ListNode(
            0, head
        )  # crea un objeto del tipo listnode con un nodo de valor 0 y siguiente la cadena
        current = dummy_head.next
        seen = 0

        n_elem = 0
        while current:
            current = current.next
            n_elem += 1

        current = dummy_head
        while current:
            if seen != n_elem - n:
                current.next = current.next.next
            current = current.next
            seen += 1
        return dummy_head.next


if __name__ == "__main__":
    sol = Solution()
    print(to_list(sol.removeNthFromEnd(build_list([0, 1, 2]), 1)))
