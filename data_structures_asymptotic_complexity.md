---
aliases: [DSA, Algorithms, Complexity, Data Structures]
tags: [academics, computer-science, algorithms, programming]
created: 2026-09-19
up: "[[About/Omar_Elnemr_Bio]]"
related: ["[[Technical/Skills_and_Stack]]"]
---

# 🧮 Data Structures & Asymptotic Complexity

Comprehensive study notes covering foundational Computer Science algorithmic principles from [[About/Omar_Elnemr_Bio#Education|University of the People and Syrian Virtual University]] coursework.

---

## 1. Asymptotic Complexity & Big-$O$ Theory

Asymptotic analysis evaluates algorithmic efficiency as the input size $n$ tends toward infinity ($n \to \infty$).

```
             Complexity Growth Hierarchy
  O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!)
  ─────── Optimal ─────── │ ──── Acceptable ─── │ ── Impractical ──
```

### Formal Mathematical Definition of Big-$O$
A function $f(n) \in O(g(n))$ if and only if there exist positive constants $c > 0$ and $n_0 \ge 0$ such that:

$$0 \le f(n) \le c \cdot g(n) \quad \forall \; n \ge n_0$$

### Standard Complexity Classes

| Notation | Name | Archetypal Example |
| :--- | :--- | :--- |
| $O(1)$ | Constant | Array index access, Hash map key lookup (average) |
| $O(\log n)$ | Logarithmic | Binary search in a sorted array |
| $O(n)$ | Linear | Single traversal, linear search |
| $O(n \log n)$ | Linearithmic | Merge Sort, Quick Sort (average case), Heap Sort |
| $O(n^2)$ | Quadratic | Bubble sort, nested pairwise comparison loops |
| $O(2^n)$ | Exponential | Recursive Fibonacci without memoization |

---

## 2. Linear Structures vs. Binary Search Trees

### Spatial Locality: Array vs. Linked List
- **Contiguous Arrays:** Elements occupy sequential memory addresses. Excellent CPU cache line prefetching ($\text{Spatial Locality}$). Insertion at arbitrary indices requires $O(n)$ shift operations.
- **Linked Lists:** Elements are stored in fragmented heap memory linked by pointer addresses. Insertion at known pointer is $O(1)$, but cache misses increase significantly.

### Binary Search Tree (BST) Invariant
For any node $N$ in a BST:
- Every key in the **left subtree** of $N$ must satisfy: $\text{Key}_{\text{left}} < \text{Key}_N$
- Every key in the **right subtree** of $N$ must satisfy: $\text{Key}_{\text{right}} > \text{Key}_N$

```
          [ 50 ]
         /      \
      [ 30 ]   [ 70 ]
      /    \   /    \
    [20]  [40][60]  [80]
```

- **Height ($h$):** A balanced BST has height $h = \lfloor \log_2 n \rfloor$. Operations (Search, Insert, Delete) execute in $O(h) = O(\log n)$.
- **Degenerate BST:** If elements are inserted sorted, the tree devolves into a singly-linked chain where $h = n$, dropping search efficiency to $O(n)$. Balanced variants (AVL, Red-Black) maintain height through rotational pivots.

---

## 3. Graph Traversal & Shortest Path Algorithms

### Breadth-First Search (BFS) vs. Depth-First Search (DFS)
- **BFS (Queue-driven):** Explores neighbors level by level. Ideal for unweighted shortest path queries. Space complexity: $O(V)$.
- **DFS (Stack/Recursion-driven):** Plunges along path depth before backtracking. Ideal for topological sorting, cycle detection, and maze solving.

### Dijkstra’s Single-Source Shortest Path
Finds the shortest distance from a start node $s$ to all other vertices in a weighted graph with non-negative edge weights $w(u, v) \ge 0$.

```python
import heapq

def dijkstra(graph, start_vertex):
    # Initialize distances with infinity
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start_vertex] = 0
    
    # Priority queue stores (distance, vertex)
    pq = [(0, start_vertex)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # Stale priority queue entry check
        if current_dist > distances[u]:
            continue
            
        for v, weight in graph[u].items():
            # Edge relaxation condition: d(v) > d(u) + w(u, v)
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                heapq.heappush(pq, (distances[v], v))
                
    return distances
```

**Complexity with Min-Heap:** $O((|V| + |E|) \log |V|)$