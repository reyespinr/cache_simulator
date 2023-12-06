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

        # Access addresses that map to the same set
        addresses = [0x100, 0x200, 0x300, 0x400]
        for address in addresses:
            cache.read_address(address)
            # print(f"After accessing {hex(address)}:")
            # print_cache_state()

        # The least recently used address (0x100) should be evicted
        self.assertIsNone(self.find_in_cache(cache, 0x100))
        # The next least recently used address (0x200) should also be evicted
        self.assertIsNone(self.find_in_cache(cache, 0x200))
        # The more recently used addresses should be retained
        self.assertIsNotNone(self.find_in_cache(cache, 0x300))
        self.assertIsNotNone(self.find_in_cache(cache, 0x400))

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

    def test_minimum_blocks(self):
        # Test with the minimum number of blocks
        block_size = 32
        config = CacheConfig(block_size=block_size, num_blocks=1,
                             associativity=1, replacement_policy='LRU')
        cache = Cache(config)

        # Simulate cache accesses with a valid address
        address = 0x100
        result = cache.read_address(address)

        self.assertFalse(
            result, "Expected cache miss for the minimum number of blocks.")

    def test_maximum_blocks(self):
        # Test with a large number of blocks (smaller than the maximum)
        block_size = 32
        num_blocks = 2**16  # A large number of blocks
        config = CacheConfig(block_size=block_size, num_blocks=num_blocks,
                             associativity=1, replacement_policy='LRU')
        cache = Cache(config)

        # Simulate cache accesses with multiple valid addresses
        addresses = [0x100, 0x200, 0x300, 0x400]

        # Ensure cache misses for all addresses
        for address in addresses:
            result = cache.read_address(address)
            self.assertFalse(
                result, f"Expected cache miss for address {hex(address)}")

    def test_minimum_associativity(self):
        # Test with minimum associativity (1)
        block_size = 32
        num_blocks = 8
        config = CacheConfig(block_size=block_size, num_blocks=num_blocks,
                             associativity=1, replacement_policy='LRU')
        cache = Cache(config)

        # Simulate cache accesses with a valid address
        address = 0x100
        result = cache.read_address(address)

        self.assertFalse(
            result, "Expected cache miss for the minimum associativity (1).")

    def test_maximum_associativity(self):
        # Test with maximum associativity (num_blocks)
        block_size = 32
        num_blocks = 8
        config = CacheConfig(block_size=block_size, num_blocks=num_blocks,
                             associativity=num_blocks, replacement_policy='LRU')
        cache = Cache(config)

        # Simulate cache accesses with a valid address
        address = 0x100
        result = cache.read_address(address)

        self.assertFalse(
            result, "Expected cache miss for the maximum associativity (num_blocks).")

    def test_edge_memory_addresses(self):
        # Test with address 0x0
        block_size = 32
        num_blocks = 4
        config = CacheConfig(block_size=block_size, num_blocks=num_blocks,
                             associativity=2, replacement_policy='LRU')
        cache = Cache(config)

        # Simulate cache accesses with address 0x0
        address = 0x0
        result = cache.read_address(address)

        self.assertFalse(
            result, "Expected cache miss for memory address 0x0.")

        # Test with the highest possible address
        max_address = 0xFFFFFFFF  # Maximum 32-bit address
        result = cache.read_address(max_address)

        self.assertFalse(
            result, "Expected cache miss for the highest possible memory address.")

    def test_invalid_inputs(self):
        # Test with invalid command-line arguments
        block_size = 32
        num_blocks = 4
        associativity = 2
        replacement_policy = 'INVALID'

        # Wrap cache configuration and initialization in a try-except block
        try:
            config = CacheConfig(block_size=block_size, num_blocks=num_blocks,
                                 associativity=associativity, replacement_policy=replacement_policy)
            cache = Cache(config)
        except ValueError as e:
            self.assertIn("Invalid configuration: replacement_policy", str(e))
        else:
            self.fail("Expected ValueError to be raised")


if __name__ == '__main__':
    unittest.main()
