"""
LeetCode 25 - Reverse Nodes in k-Group (Hard)

Problem: Given the head of a linked list, reverse the nodes of the list k at a time and return
the modified list. If the number of nodes is not a multiple of k, the left-out nodes at the end
remain as they are. Only the nodes themselves may be changed, not their values.
(1 <= k <= number of nodes = L <= 5000, 0 <= Node.val <= 1000)
Follow up: can you solve it in O(1) extra memory?

Approach 1 - Store each group in a list and relink it (reverseKGroup):
    Key idea: count the nodes first; only L // k full groups are reversed and the leftover
    stays. For each group, keep prev on the node BEFORE the group and store its k nodes in a
    list, so every node has a name before any arrow changes. Save next_group, then relink:

        before: prev -> g[0] -> g[1] -> ... -> g[k-1] -> next_group
        after:  prev -> g[k-1] -> ... -> g[1] -> g[0] -> next_group

        - inner arrows: g[j].next = g[j - 1], for j = k - 1 down to 1
        - ends: prev.next = g[k-1] (new first) and g[0].next = next_group (new last)
        - g[0] is now the last node of the group, so it becomes prev for the next group.

    Complexity (L = number of nodes):
        Time:  O(L) -> one pass to count, then L // k groups with O(k) work each:
               (L // k) * k <= L.
        Space: O(k) -> the list holds the k nodes of ONE group at a time; it is rebuilt for
               every group, so it never grows beyond k. The nodes are relinked, not copied.

    Note:
        - range with a negative step goes from the larger to the smaller value:
          range(k - 1, 0, -1) gives k - 1, ..., 1, while range(1, k, -1) is empty.
        - The new first of the group is the old LAST (g[k-1]) and the new last is the old
          FIRST (g[0]): prev must point to g[k-1], and g[0] links to the next group.
        - Save next_group before changing any arrow, or the rest of the list is lost.
        - Follow up, O(1) space: reverse each group in place with three pointers
          (prev, curr, next), the technique of LeetCode 206 (Reverse Linked List).
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
    def reverseKGroup(self, head: ListNode | None, k: int) -> ListNode | None:
        """Reverse every full group of k nodes, storing each group in a list."""
        dummy = ListNode(0, head)
        prev = dummy  # node before the current group

        # Count the nodes: only full groups are reversed
        n_nodes = 0
        current = head
        while current:
            n_nodes += 1
            current = current.next

        for _ in range(n_nodes // k):  # only full groups are reversed; the rest stays
            group = [prev.next]
            for _ in range(k - 1):  # exactly k nodes
                group.append(group[-1].next)
            next_group = group[-1].next  # save it BEFORE changing any arrow

            for j in range(
                k - 1, 0, -1
            ):  # inner arrows: each node points to the previous one
                group[j].next = group[j - 1]

            prev.next = group[-1]  # prev -> new first (old last)
            group[0].next = next_group  # new last (old first) -> next group
            prev = group[0]  # new last is the prev of the next group

        return dummy.next


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),  # leftover group stays
        ([1, 2, 3, 4, 5, 6], 3, [3, 2, 1, 6, 5, 4]),  # exact groups
        ([1, 2, 3, 4, 5, 6, 7], 3, [3, 2, 1, 6, 5, 4, 7]),
        ([1, 2, 3, 4], 4, [4, 3, 2, 1]),  # k == length: whole list reversed
        ([1, 2, 3], 1, [1, 2, 3]),  # k == 1: nothing changes
        ([1], 1, [1]),  # single node
        ([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]),  # same as LeetCode 24 when k == 2
    ]

    for values, k, expected in test_cases:
        result = to_list(sol.reverseKGroup(build_list(values), k))
        assert result == expected, (values, k, result)

    # Brute-force check: reverse full chunks of a Python list and compare
    for length in range(1, 13):
        for k in range(1, length + 1):
            values = list(range(length))
            expected = []
            for start in range(0, length, k):
                chunk = values[start : start + k]
                expected += chunk[::-1] if len(chunk) == k else chunk
            result = to_list(sol.reverseKGroup(build_list(values), k))
            assert result == expected, (length, k, result)

    print("OK")
