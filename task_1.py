"""
Реалізуйте програму для оптимізації обробки запитів до масиву чисел за допомогою LRU-кешу.



Технічні умови

1. Дано масив розміром N, який складається з позитивних цілих чисел (1 ≤ N ≤ 100_000).
 Потрібно обробити Q запитів (1 ≤ Q ≤ 50_000) такого типу:

Range(L, R) — знайти суму елементів на відрізку від індексу L до R включно.
Update(index, value) — замінити значення елемента в масиві за індексом index на нове значення value.
2. Реалізуйте чотири функції для роботи з масивом:


Функція має обчислювати суму елементів масиву на відрізку від L до R включно без використання кешу.
Для кожного запиту результат має обчислюватися заново.

update_no_cache(array, index, value)
Функція має оновлювати значення елемента масиву за вказаним індексом без використання кешу.
"""

# pylint: disable=invalid-name


import argparse
from timeit import timeit
from random import randint, choice
from collections import OrderedDict, Counter

argparser = argparse.ArgumentParser()
argparser.add_argument("--same_queries", type=int, default=30000)
args = argparser.parse_args()


class LRUCache:
    """LRU Cache implementation."""

    def __init__(self, capacity: int = 1000):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, L: int, R: int) -> int | None:
        """Get the value of the key if the key exists in the cache."""
        key = (L, R)
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, L: int, R: int, value: int):
        """Put the value of the key if the key does not exist in the cache."""
        key = (L, R)
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate_index(self, index: int):
        """Invalidate the cache for the given index."""
        to_delete = [k for k in self.cache if k[0] <= index <= k[1]]
        for k in to_delete:
            del self.cache[k]


cache_for_range_sum = LRUCache()


def range_sum_no_cache(array: list[int], L: int, R: int) -> int:
    """
    Function to calculate the sum of elements in the array from index L to R (inclusive)
    without using a cache and using custom loop.
    For each query, the result is calculated from scratch.
    """
    result = 0
    for i in range(L, R + 1):
        result += array[i]
    return result


def range_sum_with_cache(array: list[int], L: int, R: int) -> int:
    """
    Function to calculate the sum of elements in the array from index L to R (inclusive)
    using a cache and using custom loop.
    """
    result = cache_for_range_sum.get(L, R)
    if result is not None:
        return result
    result = 0
    for i in range(L, R + 1):
        result += array[i]
    cache_for_range_sum.put(L, R, result)
    return result


def update_no_cache(array: list[int], index: int, value: int):
    """Function to update the value of an element in the array at a specific index."""
    array[index] = value
    return array


def update_with_cache(array: list[int], index: int, value: int):
    """Function to update the value of an element in the array at a specific index using a cache."""
    array[index] = value
    cache_for_range_sum.invalidate_index(index)
    return array


def get_random(array_size: int) -> int:
    """Function to get a random number."""
    return randint(0, array_size - 1)


def generate_array_and_queries(
    query_count: int = 50000, same_queries: int = 30000, array_size: int = 100000
):
    """Function to generate queries."""
    array_ = [randint(1, 100) for _ in range(array_size)]
    queries = []
    stable_left, stable_value = get_random(array_size), randint(1, 100)
    stable_right = sorted((stable_left, get_random(array_size)))[1]
    for _ in range(same_queries):
        func_type = choice(["Range", "Update"])
        if func_type == "Update":
            left, right = stable_left, stable_value
        else:
            left, right = stable_left, stable_right
        queries.append((func_type, left, right))

    for _ in range(query_count - same_queries):
        func_type = choice(["Range", "Update"])
        if func_type == "Update":
            left, right = get_random(array_size), randint(1, 100)
        else:
            left, right = sorted((get_random(array_size), get_random(array_size)))
        queries.append((func_type, left, right))
    return array_, queries


def show_queries_stat(queries: list[tuple[str, int, int]]):
    """Function to show queries statistics."""
    range_queries = [query for query in queries if query[0] == "Range"]
    update_queries = [query for query in queries if query[0] == "Update"]
    print(f"Range queries: {len(range_queries)}")
    print(f"Update queries: {len(update_queries)}")
    print(f"Total queries: {len(queries)}")
    range_counts = Counter((L, R) for _, L, R in range_queries)

    print("\nMost common Range queries (L, R):")
    for (L, R), count in range_counts.most_common(2):
        print(f"({L}, {R}): {count} times")

    # Count index updates for update queries
    update_counts = Counter((L, R) for _, L, R in update_queries)

    print("\nMost common Update indices:")
    for (L, R), count in update_counts.most_common(2):
        print(f"({L}, {R}): updated {count} times")
    print(f"Range queries percentage: {len(range_queries) / len(queries) * 100}")
    print(f"Update queries percentage: {len(update_queries) / len(queries) * 100}")


def main():
    """Main function to run the test."""
    same_queries = args.same_queries
    array_, queries = generate_array_and_queries(same_queries=same_queries)
    show_queries_stat(queries)
    # print(queries)
    print("-" * 50)

    def run_test_no_cache():
        """Function to run the test."""
        for query in queries:
            func_type, L, R = query
            if func_type == "Range":
                range_sum_no_cache(array_, L, R)
            elif func_type == "Update":
                update_no_cache(array_, L, R)

    def run_test_with_cache():
        """Function to run the test."""
        for query in queries:
            func_type, L, R = query
            if func_type == "Range":
                range_sum_with_cache(array_, L, R)
            elif func_type == "Update":
                update_with_cache(array_, L, R)

    elapsed_time_no_cache = timeit(run_test_no_cache, number=1)
    elapsed_time_with_cache = timeit(run_test_with_cache, number=1)

    print("Elapsed time no cache:", elapsed_time_no_cache)
    print("Elapsed time with cache:", elapsed_time_with_cache)


if __name__ == "__main__":
    main()
