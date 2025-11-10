"""Hash table with chaining (separate chaining) and a universal-style hash function.

Provides:
- HashTableChaining: insert, search (raises KeyError), get (with default), delete
- __contains__, __len__, keys, items, values helpers

The hash function is of the multiply-add modulo prime family:
	h(k) = ((a * hash(k) + b) mod p) mod m
where a and b are chosen at construction time to reduce adversarial collisions.
"""

from __future__ import annotations

import random
from typing import Any, Iterator, List, Optional, Tuple
import time


class HashTableChaining:
	"""Hash table using separate chaining for collisions.

	Args:
		capacity: number of chains (table size). Prefer a prime for slightly better distribution.
		seed: optional integer seed for deterministic choices of the universal hash params.
	"""

	def __init__(self, capacity: int = 101, seed: Optional[int] = None) -> None:
		if capacity <= 0:
			raise ValueError("capacity must be positive")
		self.m = capacity
		# large prime for universal hashing (use a big 61-bit prime)
		self.p = (1 << 61) - 1  # 2^61 - 1, a Mersenne prime

		self._rand = random.Random(seed)
		# choose a in [1, p-1], b in [0, p-1]
		self.a = self._rand.randrange(1, self.p)
		self.b = self._rand.randrange(0, self.p)

		# chains: each entry is a list of (key, value) pairs
		self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.m)]
		self.n = 0

	def _hash(self, key: Any) -> int:
		# use Python's built-in hash to obtain an integer; allow negative values
		k = hash(key)
		# ensure k is an integer within Python's integer range; Python's ints are unbounded
		# compute universal-style hash and reduce to table size
		# convert k to non-negative by modulo p (works with negative k too)
		k_mod = k % self.p
		return ((self.a * k_mod + self.b) % self.p) % self.m

	def insert(self, key: Any, value: Any) -> None:
		"""Insert or update a key with the given value."""
		idx = self._hash(key)
		chain = self.table[idx]
		for i, (k, _) in enumerate(chain):
			if k == key:
				chain[i] = (key, value)
				return
		chain.append((key, value))
		self.n += 1

	def search(self, key: Any) -> Any:
		"""Return the value associated with key. Raises KeyError if not present."""
		idx = self._hash(key)
		chain = self.table[idx]
		for k, v in chain:
			if k == key:
				return v
		raise KeyError(key)

	def get(self, key: Any, default: Any = None) -> Any:
		"""Return value for key if present, otherwise default."""
		try:
			return self.search(key)
		except KeyError:
			return default

	def delete(self, key: Any) -> None:
		"""Remove key from table. Raises KeyError if key not found."""
		idx = self._hash(key)
		chain = self.table[idx]
		for i, (k, _) in enumerate(chain):
			if k == key:
				del chain[i]
				self.n -= 1
				return
		raise KeyError(key)

	def __len__(self) -> int:
		return self.n

	def __contains__(self, key: Any) -> bool:
		try:
			self.search(key)
			return True
		except KeyError:
			return False

	def keys(self) -> Iterator[Any]:
		for chain in self.table:
			for k, _ in chain:
				yield k

	def values(self) -> Iterator[Any]:
		for chain in self.table:
			for _, v in chain:
				yield v

	def items(self) -> Iterator[Tuple[Any, Any]]:
		for chain in self.table:
			for k, v in chain:
				yield (k, v)

	def __repr__(self) -> str:  # pragma: no cover - small helper
		items = list(self.items())
		return f"HashTableChaining(m={self.m}, n={self.n}, items={items})"



def add_n_elements(ht: HashTableChaining | None, n: int, *, start: int = 0, key_prefix: str = "k") -> HashTableChaining:
	"""Insert n sequential elements into the hash table.

	If `ht` is None a new `HashTableChaining` is created with a capacity chosen
	to keep the initial load factor modest. Keys are generated as
	`{key_prefix}{i}` and values are the integer `i`.

	Args:
		ht: Optional HashTableChaining to populate. If None, a new table is created.
		n: Number of elements to insert (n >= 0).
		start: Starting index for keys/values (default 0).
		key_prefix: Prefix for generated keys (default 'k').

	Returns:
		The hash table that was populated (either the provided `ht` or the newly created one).
	"""
	if n < 0:
		raise ValueError("n must be non-negative")
	if ht is None:
		# choose capacity so load factor is roughly <= 0.5 initially
		capacity = max(11, (n // 2) + 1)
		ht = HashTableChaining(capacity=capacity)

	for i in range(start, start + n):
		ht.insert(f"{key_prefix}{i}", i)

	return ht


if __name__ == "__main__":
	# Measure total time for the following sequence:
	# 1) add 10,000 items
	# 2) search 50 existing keys and 50 non-existing keys
	# 3) delete 100 keys
	import random as _random

	start_time = time.perf_counter()

	ht = add_n_elements(None, 10_000)

	rng = _random.Random(12345)
	# pick 50 existing keys (sample without replacement)
	existing_indices = rng.sample(range(0, 10_000), 50)
	existing_keys = [f"k{i}" for i in existing_indices]

	# create 50 keys that are not present
	non_existing_keys = [f"k{10_000 + i}" for i in range(50)]

	# perform searches
	found_existing = 0
	found_non_existing = 0
	for key in existing_keys:
		try:
			_ = ht.search(key)
			found_existing += 1
		except KeyError:
			pass
	for key in non_existing_keys:
		try:
			_ = ht.search(key)
			found_non_existing += 1
		except KeyError:
			pass

	# delete 100 keys
	delete_indices = rng.sample(range(0, 10_000), 100)
	deleted = 0
	for i in delete_indices:
		try:
			ht.delete(f"k{i}")
			deleted += 1
		except KeyError:
			pass

	end_time = time.perf_counter()
	total = end_time - start_time

	print(
		"Total time for add 10,000 + 50 existing searches + 50 non-existing searches + delete 100:",
		f"{total:.6f} seconds",
	)
	print(f"Found existing: {found_existing}/50; Found non-existing (unexpected): {found_non_existing}/50")
	print(f"Successfully deleted: {deleted}/100; Remaining items: {len(ht)}")

