import unittest
import math
from src.cache import Cache
from src.config import CacheConfig


class TestCache(unittest.TestCase):
    """
    A test suite for the Cache and CacheLine classes.

    This test suite includes various test cases to ensure the correctness of the cache simulator.
    """

    def test_get_set_index_and_tag(self):
        """
        Test the get_set_index_and_tag method.

        This test case checks if the get_set_index_and_tag method correctly calculates set index and tag from a memory address.
        """
        # Test with a specific address
        block_size = 32
        num_blocks = 4
        associativity = 2
        num_sets = num_blocks // associativity

        config = CacheConfig(block_size=block_size, num_blocks=num_blocks,
                             associativity=associativity, replacement_policy='LRU')
        cache = Cache(config)

        address = 0x12345678
        set_index, tag = cache.get_set_index_and_tag(address)

        # Calculate expected values based on cache.py logic
        block_offset_bits = int(math.log2(block_size))
        set_index_bits = int(math.log2(num_sets))
        expected_set_index = (address >> block_offset_bits) & (
            (1 << set_index_bits) - 1)
        expected_tag = address >> (block_offset_bits + set_index_bits)

        self.assertEqual(set_index, expected_set_index)
        self.assertEqual(tag, expected_tag)

    def test_lru_policy(self):
        """
        Test the LRU replacement policy.

        This test case checks if the LRU replacement policy correctly evicts the least recently used cache lines.
        """
        config = CacheConfig(block_size=32, num_blocks=8,
                             associativity=2, replacement_policy='LRU')
        cache = Cache(config)

        # Debug function to print the state of the cache lines
        def print_cache_state():
            for i, set_ in enumerate(cache.sets):
                print(
                    f"Set {i}: {[f'Tag: {line.tag}, Last Used: {line.last_used}' for line in set_]}")

        addresses = [0x100, 0x200, 0x300, 0x400]
        for address in addresses:
            cache.read_address(address)

        # The least recently used address (0x100) should be evicted
        self.assertIsNone(self.find_in_cache(cache, 0x100))
        # The next least recently used address (0x200) should also be evicted
        self.assertIsNone(self.find_in_cache(cache, 0x200))
        # The more recently used addresses should be retained
        self.assertIsNotNone(self.find_in_cache(cache, 0x300))
        self.assertIsNotNone(self.find_in_cache(cache, 0x400))

    def find_in_cache(self, cache, address):
        """
        Helper function to find a cache line in the cache.

        Args:
            cache (Cache): The Cache object.
            address (int): The memory address to search for in the cache.

        Returns:
            CacheLine or None: The CacheLine object if found, else None.
        """
        set_index, tag = cache.get_set_index_and_tag(address)
        set_ = cache.sets[set_index]
        for line in set_:
            if line.tag == tag:
                return line
        return None

    def test_cache_hit_miss(self):
        """
        Test cache hits and misses.

        This test case checks for cache hits and misses by accessing a block.
        It expects a cache miss for the first access and a cache hit for the second access.
        """
        config = CacheConfig(block_size=32, num_blocks=4,
                             associativity=2, replacement_policy='LRU')
        cache = Cache(config)

        # Access a block, expect a miss, then a hit
        address = 0x300
        self.assertFalse(cache.read_address(address))  # Expect miss
        self.assertTrue(cache.read_address(address))   # Expect hit

    def test_cache_read_operations(self):
        """
        Test cache read operations.

        This test case simulates cache read operations in different sets.
        It expects cache misses for initial accesses and cache hits for subsequent accesses.
        """
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

    def test_cache_configuration(self):
        """
        Test cache configuration.

        This test case checks cache behavior with different configurations, including small sets and large block sizes.
        """
        # Test with a small number of sets
        small_config = CacheConfig(
            block_size=32, num_blocks=2, associativity=1, replacement_policy='LRU')
        small_cache = Cache(small_config)
        self.assertFalse(small_cache.read_address(0x100))  # Expect miss
        self.assertTrue(small_cache.read_address(0x100))   # Expect hit

        # Additional configuration tests can be added here...

    def test_minimum_blocks(self):
        """
        Test cache with the minimum number of blocks.

        This test case checks cache behavior with the minimum number of blocks.
        """
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
        """
        Test cache with a large number of blocks (smaller than the maximum).

        This test case checks cache behavior with a large number of blocks.
        It expects cache misses for all addresses.
        """
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
        """
        Test cache with minimum associativity (1).

        This test case checks cache behavior with the minimum associativity.
        """
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
        """
        Test cache with maximum associativity (num_blocks).

        This test case checks cache behavior with the maximum associativity.
        """
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
        """
        Test cache behavior with edge memory addresses.

        This test case checks cache behavior with edge memory addresses (0x0 and the highest possible address).
        It expects cache misses for both addresses.
        """
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
        """
        Test invalid command-line arguments.

        This test case checks if the cache simulator handles invalid configuration inputs.
        """
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
