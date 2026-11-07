"""
LeetCode 23 - Merge K Sorted Lists (Hard)

Problem: You are given an array of k linked lists, each sorted in ascending order. Merge all
the linked lists into one sorted linked list and return it.
(0 <= k <= 10^4, 0 <= len(lists[i]) <= 500, -10^4 <= Node.val <= 10^4,
total number of nodes N <= 10^4)

Approach 1 - Pick the minimum head among the k lists (mergeKLists):
    Key idea: generalization of merging two lists (LeetCode 21). Keep a dummy node and a tail
    pointer. Drop the empty lists once; then, while some list is left, find the list whose
    head has the minimum value, attach that head to tail, advance tail and advance that list.
    When a list is exhausted, remove it, so lists only contains non-empty lists and the loop
    stops when all of them are used.

    Complexity (N = total number of nodes, k = number of lists):
        Time:  O(N * k) -> N iterations (one per node attached), and each one scans the k
               current heads to find the minimum.
        Space: O(k) -> the filtered list of heads. No new nodes are created: the existing
               ones are relinked.

    Note:
        - key expects a FUNCTION: key=lambda i: lists[i].val means "compare index i by the
          value of the head of lists[i]". min returns the element of the iterable (the index),
          not the key.
        - min over range(len(lists)) finds the index in one pass; lists.index(min(lists, ...))
          would scan twice.
        - Filtering once before the loop + popping exhausted lists keeps None out of min.
          `while lists` with [None, None] would be True: a non-empty list is truthy.

Approach 2 - Divide and conquer: merge in pairs, like a tournament
(mergeKLists_divideAndConquer):
    Key idea: reuse the two-list merge of LeetCode 21. In every round, merge the lists in
    pairs (0 with 1, 2 with 3, ...); the survivors play the next round. If the number of lists
    is odd, the last one has no opponent: it is merged with None, so it passes unchanged.
    Stop when one list is left.

        l1 + l2 | l3 + l4 | l5 + l6 | l7 + l8      (8 lists)
            w12 + w34 | w56 + w78                 (4 lists)
                w1234 + w5678                     (2 lists)
                    w12345678                     (1 list)

    Complexity (N = total number of nodes, k = number of lists):
        Time:  O(N log k) -> in every round each node is moved exactly once, O(N) per round,
               and the number of lists halves every round, so there are ceil(log2 k) rounds.
        Space: O(k) -> the list of survivors of each round (k / 2, k / 4, ...). The merge
               itself relinks nodes in place.

    Note:
        - Optimal for this problem: with k = 10^4, log2 k ~ 14 instead of a factor 10^4.
        - Same idea as merge sort: the merge step is the one from LeetCode 21.
        - Each round must start with an EMPTY survivors list and then replace lists; using
          len(lists) directly (instead of a stored length) keeps both in sync.
        - Empty input lists need no special treatment: merging with None returns the other.
        - Alternative with the same complexity: a min-heap (heapq) with the k current heads,
          each push/pop costs O(log k).
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
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        """Repeatedly attach the smallest head among the k lists to the result."""
        dummy = ListNode()  # placeholder in front of the merged list
        tail = dummy  # last node of the merged list

        lists = [head for head in lists if head]  # drop empty lists once
        while lists:  # stops when every list is exhausted
            idx = min(
                range(len(lists)), key=lambda i: lists[i].val
            )  # index of min head
            tail.next = lists[idx]
            tail = tail.next
            lists[idx] = lists[idx].next

            if not lists[idx]:  # this list is exhausted
                lists.pop(idx)

        return dummy.next

    def mergeKLists_divideAndConquer(
        self, lists: list[ListNode | None]
    ) -> ListNode | None:
        """Merge the lists in pairs, round after round, until only one is left."""

        def _mergeTwoLists(
            list1: ListNode | None, list2: ListNode | None
        ) -> ListNode | None:
            """Merge two sorted lists (LeetCode 21)."""
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

        while len(lists) > 1:  # one round of the tournament
            survivors = []
            for fighter in range(0, len(lists), 2):
                opponent = lists[fighter + 1] if fighter + 1 < len(lists) else None
                survivors.append(_mergeTwoLists(lists[fighter], opponent))
            lists = survivors  # the winners play the next round

        return lists[0] if lists else None  # None if k == 0


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
        ([], []),  # no lists
        ([[]], []),  # one empty list
        ([[], [1]], [1]),  # empty + non-empty
        ([[2], [], [1]], [1, 2]),  # empty in the middle
        ([[1, 1], [1], [1, 1, 1]], [1, 1, 1, 1, 1, 1]),  # all equal
        ([[-3, 0, 7], [-5, 2], [8, 9], [-10]], [-10, -5, -3, 0, 2, 7, 8, 9]),
        ([[i] for i in range(10, 0, -1)], list(range(1, 11))),  # 10 -> 5 -> 3 -> 2 -> 1
        ([[1, 2, 3]], [1, 2, 3]),  # a single list: no rounds at all
    ]

    for method in (sol.mergeKLists, sol.mergeKLists_divideAndConquer):
        for lists_values, expected in test_cases:
            result = to_list(method([build_list(v) for v in lists_values]))
            assert result == expected, (method.__name__, lists_values, result)
        print(f"{method.__name__}: OK")
