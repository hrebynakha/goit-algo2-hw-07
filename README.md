# goit-algo2-hw-07

### Task 1


LRU cache implementation with  class `LRUCache` and  using `OrderedDict` from `collections` module

Write a program to optimize query processing to an array of numbers using an LRU cache.

functions:
- `range_sum_no_cache` - function to calculate the sum of elements in the array from index L to R (inclusive) without using a cache and using custom loop.
- `range_sum_with_cache` - function to calculate the sum of elements in the array from index L to R (inclusive) using a cache and using custom loop.
- `update_no_cache` - function to update the value of an element in the array at a specific index.
- `update_with_cache` - function to update the value of an element in the array at a specific index using a cache.


Helper functions:
- `get_random` - function to get a random number.
- `generate_array_and_queries` - function to generate queries.
- `show_queries_stat` - function to show queries statistics.


### Example output

Runing with same queries 30000 (default value)

```bash
python task_1.py
```

Output (function with cache works faster):

```
Range queries: 25064
Update queries: 24936
Total queries: 50000

Most common Range queries (L, R):
(2887, 55322): 15147 times
(8494, 9290): 1 times

Most common Update indices:
(2887, 94): updated 14853 times
(15151, 74): updated 2 times
Range queries percentage: 50.12799999999999
Update queries percentage: 49.872
--------------------------------------------------
Elapsed time no cache: 35.87086488299974
Elapsed time with cache: 23.652526636999937
```

Runing with same queries 0



```bash
python task_1.py --same_queries 0
```

Output (function with cache works slower):

```
Range queries: 25007
Update queries: 24993
Total queries: 50000

Most common Range queries (L, R):
(60740, 90792): 1 times
(7701, 67993): 1 times

Most common Update indices:
(3907, 45): updated 2 times
(58111, 82): updated 2 times
Range queries percentage: 50.014
Update queries percentage: 49.986000000000004
--------------------------------------------------
Elapsed time no cache: 27.858260871999846
Elapsed time with cache: 28.885637047999808
```


### Conclusion


The function `range_sum_with_cache` is faster than the function `range_sum_no_cache` because it uses a cache to store the results of previous queries, so it can reuse the results of previous queries instead of recalculating them. It faster only if we have a lot of queries to the same range. ( in this case it is 30000 queries to the same range) . But if we don't have a lot of queries to the same range, the function `range_sum_no_cache` is faster. 

Function `update_with_cache` not faster becouse in case whent we used cache, we need to invalidate cache for the given index, so it a new operation that takes time. 



### Task 2






### Output

```bash
python task_2.py
```

Output time table results for fibonacci numbers calculation:

```


----------------------------------------------------
| Fibonacci numbers  | LRU          |   Splay      |
----------------------------------------------------
| 0                  |  0.000016    |  0.000957    |
| 50                 |  0.000033    |  0.000168    |
| 100                |  0.000059    |  0.000280    |
| 150                |  0.000068    |  0.000267    |
| 200                |  0.000105    |  0.000319    |
| 250                |  0.000074    |  0.000403    |
| 300                |  0.000098    |  0.000512    |
| 350                |  0.000242    |  0.000848    |
| 400                |  0.000171    |  0.000850    |
| 450                |  0.000222    |  0.001044    |
| 500                |  0.000241    |  0.001160    |
| 550                |  0.000246    |  0.001234    |
| 600                |  0.000342    |  0.001475    |
| 650                |  0.000340    |  0.001633    |
| 700                |  0.000418    |  0.001662    |
| 750                |  0.000311    |  0.001749    |
| 800                |  0.000314    |  0.001918    |
| 850                |  0.000407    |  0.002171    |
| 900                |  0.000385    |  0.001837    |
| 950                |  0.000490    |  0.001481    |
----------------------------------------------------

```


### Conclusion

Fibonacci numbers calculation is faster with LRU cache than with Splay Tree.

This is because LRU cache is a simple and efficient way to store and retrieve previously calculated values, while Splay Tree is a more complex data structure that requires more memory and processing power to balance the tree. 