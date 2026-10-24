"""Leakage-free dataset splitting.

Product-photo datasets contain near-duplicates (same item re-cropped, re-sized or
re-coloured). Splitting per image lets copies land in both train and test, which
inflates validation scores. These helpers group near-duplicates with a perceptual
hash and split whole groups, stratified by class (plan §3.2 / Phase B1).
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np
from PIL import Image


def average_hash(image: Image.Image, hash_size: int = 8) -> int:
    """Average-hash ("aHash"): ``hash_size**2`` bits, robust to resizing and recompression."""
    small = image.convert("L").resize((hash_size, hash_size), Image.Resampling.BOX)
    pixels = np.asarray(small, dtype=np.float64)
    bits = (pixels > pixels.mean()).ravel()
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return value


def hamming_distance(a: int, b: int) -> int:
    return int(bin(int(a) ^ int(b)).count("1"))


class _UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def group_near_duplicates(hashes, max_distance: int = 4, hash_bits: int = 64) -> np.ndarray:
    """Assign a group id to every hash; hashes within ``max_distance`` bits share a group (transitively).

    Uses the pigeonhole banding trick: split hashes into ``max_distance + 1`` bands;
    two hashes within the distance must agree exactly on at least one band, so only
    hashes sharing a band value are compared. Scales to hundreds of thousands of images.
    """
    hashes = [int(h) for h in hashes]
    n = len(hashes)
    if n == 0:
        return np.zeros(0, dtype=np.int64)
    if max_distance < 0:
        raise ValueError("max_distance must be >= 0")

    uf = _UnionFind(n)
    n_bands = min(max_distance + 1, hash_bits)
    band_width = -(-hash_bits // n_bands)  # ceil division
    for band in range(n_bands):
        shift = band * band_width
        mask = (1 << band_width) - 1
        buckets: dict[int, list[int]] = defaultdict(list)
        for idx, h in enumerate(hashes):
            buckets[(h >> shift) & mask].append(idx)
        for members in buckets.values():
            if len(members) < 2:
                continue
            for i_pos, i in enumerate(members):
                for j in members[i_pos + 1:]:
                    if uf.find(i) != uf.find(j) and hamming_distance(hashes[i], hashes[j]) <= max_distance:
                        uf.union(i, j)

    roots = np.array([uf.find(i) for i in range(n)], dtype=np.int64)
    _, group_ids = np.unique(roots, return_inverse=True)
    return group_ids.astype(np.int64)


def grouped_stratified_split(labels, groups, val_fraction: float = 0.15, test_fraction: float = 0.15, seed: int = 42):
    """Split sample indices into (train, val, test) so that no group spans two splits.

    Each group is assigned to its majority class; within each class, groups are
    shuffled (seeded) and allotted to test, then val, then train, so each class
    gets close to the requested fractions. Returns three sorted index arrays.
    """
    labels = np.asarray(labels).ravel()
    groups = np.asarray(groups).ravel()
    if labels.shape != groups.shape:
        raise ValueError("labels and groups must have the same length")
    if not (0 <= val_fraction < 1 and 0 <= test_fraction < 1 and val_fraction + test_fraction < 1):
        raise ValueError("fractions must be in [0, 1) and sum to less than 1")

    members: dict[int, list[int]] = defaultdict(list)
    for idx, g in enumerate(groups.tolist()):
        members[g].append(idx)

    class_groups: dict[int, list[int]] = defaultdict(list)
    for g, idxs in members.items():
        values, counts = np.unique(labels[idxs], return_counts=True)
        majority = int(values[np.argmax(counts)])  # ties → smallest label
        class_groups[majority].append(g)

    rng = np.random.default_rng(seed)
    train, val, test = [], [], []
    for cls in sorted(class_groups):
        gs = sorted(class_groups[cls])
        rng.shuffle(gs)
        total = sum(len(members[g]) for g in gs)
        target_test, target_val = test_fraction * total, val_fraction * total
        n_test = n_val = 0
        for g in gs:
            size = len(members[g])
            if n_test + size / 2 <= target_test:
                test.extend(members[g])
                n_test += size
            elif n_val + size / 2 <= target_val:
                val.extend(members[g])
                n_val += size
            else:
                train.extend(members[g])

    return (np.array(sorted(train), dtype=np.int64),
            np.array(sorted(val), dtype=np.int64),
            np.array(sorted(test), dtype=np.int64))
