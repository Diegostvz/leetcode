"""
0002. Add Two Numbers — Medium
https://leetcode.com/problems/add-two-numbers/
Pattern: linked list / addition with carry
Complexity: O(max(m, n)) time, O(1) extra space (excluding the output list)
Notes:
- First approach: convert both lists to int, add, rebuild the list. Works in Python
  (arbitrary-precision integers) but would overflow in other languages and sidesteps
  the point of the problem.
- Final approach: add digit by digit, as by hand, propagating the carry.
  The "or carry" in the while loop handles cases like 5 + 5 = 10 (a final 1 remains).
- Dummy node: avoids special-casing the head of the result list.
"""


class ListNode:
    """LeetCode provides this definition; needed here to run locally."""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(
        self, l1: ListNode | None, l2: ListNode | None
    ) -> ListNode | None:
        dummy = ListNode()
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            carry, digit = divmod(v1 + v2 + carry, 10)

            current.next = ListNode(digit)
            current = current.next

            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next


# --- Utilidades para probar en local (no se copian a LeetCode) ---
def build(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    current = dummy
    for v in values:
        current.next = ListNode(v)
        current = current.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    sol = Solution()
    assert to_list(sol.addTwoNumbers(build([2, 4, 3]), build([5, 6, 4]))) == [7, 0, 8]
    assert to_list(sol.addTwoNumbers(build([0]), build([0]))) == [0]
    assert to_list(sol.addTwoNumbers(build([9, 9, 9, 9]), build([9, 9]))) == [
        8,
        9,
        0,
        0,
        1,
    ]
    assert to_list(sol.addTwoNumbers(build([5]), build([5]))) == [0, 1]
    print("OK")
