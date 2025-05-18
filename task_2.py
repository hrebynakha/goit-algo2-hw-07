"""
Task 2
 Порівняння продуктивності обчислення чисел Фібоначчі із використанням LRU-кешу та Splay Tree



Реалізуйте програму для обчислення чисел Фібоначчі двома способами:
 із використанням LRU-кешу та з використанням Splay Tree
 для збереження попередньо обчислених значень.
  Проведіть порівняльний аналіз їхньої ефективності,
  вимірявши середній час виконання для кожного з підходів

"""

import sys
from timeit import timeit
from functools import lru_cache


class Node:
    """Node class for Splay Tree. Changed with data to key and value."""

    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    """Splay Tree class."""

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Вставка нового елемента в дерево."""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        """Рекурсивна вставка елемента в дерево."""
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, value, current_node.left_node)
            else:
                current_node.left_node = Node(key, value, current_node)
        else:
            if current_node.right_node:
                self._insert_node(key, value, current_node.right_node)
            else:
                current_node.right_node = Node(key, value, current_node)

    def find(self, key):
        """Пошук елемента в дереві із застосуванням сплаювання."""
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)
                return node.value  # return node value instead just data
        return None  # Якщо елемент не знайдено.

    def _splay(self, node):
        """Реалізація сплаювання для переміщення вузла до кореня."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig-ситуація
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left_node
                and node.parent == node.parent.parent.left_node
            ):  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right_node
                and node.parent == node.parent.parent.right_node
            ):  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Права ротація вузла."""
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Ліва ротація вузла."""
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    """Function to calculate the n-th Fibonacci number using LRU caching."""
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, splay_tree: SplayTree):
    """Function to calculate the n-th Fibonacci number using Splay Tree."""
    if n < 2:
        splay_tree.insert(n, n)
        return n

    el = splay_tree.find(n)
    if el is not None:
        return el

    result = fibonacci_splay(n - 1, splay_tree) + fibonacci_splay(n - 2, splay_tree)
    splay_tree.insert(n, result)
    return result


def generate_fibonacci_test_number() -> list[int]:
    """Function to generate a test number."""
    nums = []
    for i in range(0, 951, 50):
        nums.append(i)
    return nums


def run_test(numbers: list[int]):
    """Function to run the test."""
    print("-" * 52)
    print(
        "| Fibonacci numbers".ljust(20),
        "| LRU ".ljust(14),
        "|   Splay   ".ljust(14),
        "|",
    )
    print("-" * 52)
    for n in numbers:
        splay_tree = SplayTree()  # Create new Splay Tree for each number
        fibonacci_lru.cache_clear()  # Clear LRU cache before timing
        elapsed_time_lru = timeit(lambda n=n: fibonacci_lru(n), number=100)
        elapsed_time_splay = timeit(
            lambda n=n, st=splay_tree: fibonacci_splay(n, st), number=100
        )
        if elapsed_time_lru < elapsed_time_splay:
            lru_color = "\033[92m"  # Green
            splay_color = "\033[91m"  # Red
        else:
            lru_color = "\033[91m"  # Red
            splay_color = "\033[92m"  # Green
        print(
            f"| {n} ".ljust(20),
            f"| {lru_color}",
            f"{elapsed_time_lru:.6f}".ljust(10),
            "\033[0m",
            f"| {splay_color}",
            f"{elapsed_time_splay:.6f}".ljust(10),
            "\033[0m",
            "|",
        )
    print("-" * 52)


def main():
    """Main function to run the test."""

    numbers = generate_fibonacci_test_number()
    sys.setrecursionlimit(5000)

    run_test(numbers)


if __name__ == "__main__":

    main()
