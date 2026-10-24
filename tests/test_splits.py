"""Tests for leakage-free splitting (training/splits.py), plan §3.2 / B1."""
import unittest

import numpy as np
from PIL import Image

from tests import ROOT  # noqa: F401
from tests.helpers import noise_image, smooth_image
from backend.fabric_classifier.training.splits import (
    average_hash,
    group_near_duplicates,
    grouped_stratified_split,
    hamming_distance,
)


class TestAverageHash(unittest.TestCase):
    def test_hash_fits_in_bit_budget(self):
        h = average_hash(noise_image(seed=1), hash_size=8)
        self.assertIsInstance(h, int)
        self.assertLess(h, 2 ** 64)

    def test_resized_copy_hashes_close(self):
        for seed in range(5):
            img = smooth_image(size=(400, 400), seed=seed)
            smaller = img.resize((200, 200), Image.Resampling.BILINEAR)
            self.assertLessEqual(hamming_distance(average_hash(img), average_hash(smaller)), 4)

    def test_jpeg_recompressed_copy_hashes_close(self):
        import io

        img = smooth_image(seed=9)
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=50)
        recompressed = Image.open(io.BytesIO(buf.getvalue()))
        self.assertLessEqual(hamming_distance(average_hash(img), average_hash(recompressed)), 4)

    def test_different_images_hash_far_apart(self):
        a, b = average_hash(smooth_image(seed=1)), average_hash(smooth_image(seed=2))
        self.assertGreater(hamming_distance(a, b), 10)

    def test_accepts_rgba_and_grayscale(self):
        rgba = noise_image(seed=4).convert("RGBA")
        gray = noise_image(seed=4).convert("L")
        self.assertIsInstance(average_hash(rgba), int)
        self.assertIsInstance(average_hash(gray), int)


class TestHamming(unittest.TestCase):
    def test_counts_differing_bits(self):
        self.assertEqual(hamming_distance(0b1011, 0b0001), 2)
        self.assertEqual(hamming_distance(7, 7), 0)


class TestGroupNearDuplicates(unittest.TestCase):
    def test_identical_hashes_share_a_group(self):
        groups = group_near_duplicates([5, 5, 1 << 40], max_distance=0)
        self.assertEqual(groups[0], groups[1])
        self.assertNotEqual(groups[0], groups[2])

    def test_near_hashes_grouped_within_distance(self):
        base = 0xF0F0F0F0F0F0F0F0
        near = base ^ 0b111  # 3 bits differ
        far = base ^ ((1 << 20) - 1)  # 20 bits differ
        groups = group_near_duplicates([base, near, far], max_distance=4)
        self.assertEqual(groups[0], groups[1])
        self.assertNotEqual(groups[0], groups[2])

    def test_grouping_is_transitive(self):
        a = 0
        b = a ^ 0b1111  # 4 from a
        c = b ^ (0b1111 << 8)  # 4 from b, 8 from a
        groups = group_near_duplicates([a, b, c], max_distance=4)
        self.assertEqual(len(set(groups.tolist())), 1)

    def test_returns_one_id_per_input(self):
        groups = group_near_duplicates(list(range(0, 1 << 30, 1 << 24)), max_distance=2)
        self.assertEqual(len(groups), len(range(0, 1 << 30, 1 << 24)))

    def test_empty_input(self):
        self.assertEqual(len(group_near_duplicates([], max_distance=4)), 0)


class TestGroupedStratifiedSplit(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(0)
        # 3 classes with an 8:3:1 imbalance; groups of 1-3 duplicates each.
        labels, groups, gid = [], [], 0
        for cls, n_groups in ((0, 800), (1, 300), (2, 100)):
            for _ in range(n_groups):
                size = int(rng.integers(1, 4))
                labels += [cls] * size
                groups += [gid] * size
                gid += 1
        self.labels = np.array(labels)
        self.groups = np.array(groups)

    def test_partition_covers_everything_once(self):
        tr, va, te = grouped_stratified_split(self.labels, self.groups, seed=1)
        allidx = np.concatenate([tr, va, te])
        self.assertEqual(len(allidx), len(self.labels))
        self.assertEqual(len(np.unique(allidx)), len(self.labels))

    def test_no_group_crosses_splits(self):
        tr, va, te = grouped_stratified_split(self.labels, self.groups, seed=1)
        sets = [set(self.groups[i].tolist()) for i in (tr, va, te)]
        self.assertFalse(sets[0] & sets[1])
        self.assertFalse(sets[0] & sets[2])
        self.assertFalse(sets[1] & sets[2])

    def test_each_class_split_close_to_requested_fractions(self):
        tr, va, te = grouped_stratified_split(self.labels, self.groups, 0.15, 0.15, seed=1)
        for cls in range(3):
            total = (self.labels == cls).sum()
            self.assertAlmostEqual((self.labels[va] == cls).sum() / total, 0.15, delta=0.04)
            self.assertAlmostEqual((self.labels[te] == cls).sum() / total, 0.15, delta=0.04)

    def test_deterministic_for_seed(self):
        a = grouped_stratified_split(self.labels, self.groups, seed=7)
        b = grouped_stratified_split(self.labels, self.groups, seed=7)
        for x, y in zip(a, b):
            np.testing.assert_array_equal(x, y)

    def test_mixed_label_group_stays_together(self):
        labels = np.array([0, 1, 0, 0, 1, 1] * 20)
        groups = np.arange(len(labels)) // 2  # every pair shares a group, pairs may mix labels
        tr, va, te = grouped_stratified_split(labels, groups, seed=0)
        for split in (tr, va, te):
            for g in set(groups[split].tolist()):
                self.assertTrue(np.all(np.isin(np.where(groups == g)[0], split)))

    def test_invalid_fractions_and_lengths_raise(self):
        with self.assertRaises(ValueError):
            grouped_stratified_split(self.labels, self.groups, 0.6, 0.5)
        with self.assertRaises(ValueError):
            grouped_stratified_split(self.labels, self.groups[:-1])


if __name__ == "__main__":
    unittest.main()
