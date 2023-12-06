import unittest
import math
from src.cache import Cache
from src.config import CacheConfig


class TestCache(unittest.TestCase):

    def test_get_set_index_and_tag(self):
        # Updated test case to align with CacheConfig calculation of num_sets
        block_size = 32
        num_blocks = 4  # Total number of blocks
        associativity = 2
        num_sets = num_blocks // associativity  # Correct calculation of num_sets

        config = CacheConfig(block_size=block_size, num_blocks=num_blocks,
                             associativity=associativity, replacement_policy='LRU')
        cache = Cache(config)

        # Test with a specific address
        address = 0x12345678
        set_index, tag = cache.get_set_index_and_tag(address)

        # Updated calculations to match cache.py logic
        block_offset_bits = int(math.log2(block_size))
        set_index_bits = int(math.log2(num_sets))
        expected_set_index = (address >> block_offset_bits) & (
            (1 << set_index_bits) - 1)
        expected_tag = address >> (block_offset_bits + set_index_bits)

        self.assertEqual(set_index, expected_set_index)
        self.assertEqual(tag, expected_tag)

    def test_lru_policy(self):
        config = CacheConfig(block_size=32, num_blocks=8,
                             associativity=2, replacement_policy='LRU')
        cache = Cache(config)

        # Debug function to print the state of the cache lines
        def print_cache_state():
            for i, set_ in enumerate(cache.sets):
                print(
                    f"Set {i}: {[f'Tag: {line.tag}, Last Used: {line.last_used}' for line in set_]}")

        # Access blocks to set their LRU status
        cache.read_address(0x100)  # Access address 0x100
        print("After accessing 0x100:")
        print_cache_state()
        cache.read_address(0x200)  # Access address 0x200, different set
        print("After accessing 0x200:")
        print_cache_state()
        cache.read_address(0x110)  # Access address 0x110, same set as 0x100
        print("After accessing 0x110:")
        print_cache_state()

        # Access a new address in the same set as 0x100
        # The least recently used block (0x100) should be replaced
        cache.read_address(0x120)
        print("After accessing 0x120:")
        print_cache_state()

        self.assertIsNone(self.find_in_cache(cache, 0x100))
        self.assertIsNotNone(self.find_in_cache(cache, 0x110))
        self.assertIsNotNone(self.find_in_cache(cache, 0x120))

    def find_in_cache(self, cache, address):
        set_index, tag = cache.get_set_index_and_tag(address)
        set_ = cache.sets[set_index]
        for line in set_:
            if line.tag == tag:
                return line
        return None

    def test_cache_hit_miss(self):
        # Test for hits and misses
        config = CacheConfig(block_size=32, num_blocks=4,
                             associativity=2, replacement_policy='LRU')
        cache = Cache(config)

        # Access a block, expect a miss, then a hit
        address = 0x300
        self.assertFalse(cache.read_address(address))  # Expect miss
        self.assertTrue(cache.read_address(address))   # Expect hit

        # Access enough blocks to cause an eviction
        # ...

        # Test with varying levels of associativity
        # ...

    def test_cache_read_operations(self):
        config = CacheConfig(block_size=32, num_blocks=8,
                             associativity=2, replacement_policy='LRU')
        cache = Cache(config)

        # Read operations in different sets
        self.assertFalse(cache.read_address(0x100))  # Expect miss in one set
        # Expect miss in another set
        self.assertFalse(cache.read_address(0x200))

        # Confirm hits after initial access
        self.assertTrue(cache.read_address(0x100))  # Expect hit
        self.assertTrue(cache.read_address(0x200))  # Expect hit

        # Test with different associativity
        # ...

    def test_cache_configuration(self):
        # Test with a small number of sets
        small_config = CacheConfig(
            block_size=32, num_blocks=2, associativity=1, replacement_policy='LRU')
        small_cache = Cache(small_config)
        self.assertFalse(small_cache.read_address(0x100))  # Expect miss
        self.assertTrue(small_cache.read_address(0x100))   # Expect hit

        # Test with a large number of sets
        # ...

        # Test with different block sizes
        # ...


if __name__ == '__main__':
    unittest.main()
