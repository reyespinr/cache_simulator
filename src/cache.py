import math
import random


class CacheLine:
    """
    Represents a single cache line with tag, data, and last used information.

    Attributes:
        tag (int): Tag value for the cache line.
        data (optional): Data stored in the cache line (optional).
        last_used (int): Last used timestamp for LRU replacement policy.

    Methods:
        No methods are defined in this class.
    """

    def __init__(self, tag=None, data=None):
        """
        Initializes a CacheLine object with the specified parameters.

        Args:
            tag (int, optional): The tag value for the cache line.
            data (optional): Data to be stored in the cache line (optional).
        """
        self.tag = tag
        self.data = data
        self.last_used = 0  # For LRU


class Cache:
    """
    Simulates a set-associative cache with support for LRU and random replacement policies.

    Attributes:
        config (CacheConfig): The configuration settings for the cache.
        sets (list): A 2D list representing cache sets and cache lines.
        access_counter (int): Counter for tracking cache access for LRU policy.

    Methods:
        get_set_index_and_tag(address): Extracts set index and tag from a memory address.
        read_address(address): Simulates a cache read operation.
        handle_miss(set_index, tag): Handles cache misses by replacing or initializing cache lines.
        print_cache_state(): Prints the current state of the cache.
    """

    # Valid replacement policies
    VALID_REPLACEMENT_POLICIES = ['LRU', 'RANDOM']

    def __init__(self, config):
        """
        Initializes a Cache object with the specified configuration.

        Args:
            config (CacheConfig): The configuration settings for the cache.

        Raises:
            ValueError: If an invalid replacement policy is provided in the configuration.
        """
        self.config = config

        # Check if the provided replacement policy is valid
        if config.replacement_policy not in self.VALID_REPLACEMENT_POLICIES:
            raise ValueError(
                "Invalid configuration: replacement_policy must be 'LRU' or 'RANDOM'")

        self.sets = [[CacheLine() for _ in range(config.associativity)]
                     for _ in range(config.num_sets)]
        self.access_counter = 0  # Used for LRU tracking

    def get_set_index_and_tag(self, address):
        """
        Extracts the set index and tag from a memory address.

        Args:
            address (int): The memory address.

        Returns:
            tuple: A tuple containing set index and tag.
        """
        block_offset_bits = int(math.log2(self.config.block_size))
        set_index_bits = int(math.log2(self.config.num_sets))

        set_index = (address >> block_offset_bits) & (
            (1 << set_index_bits) - 1)
        tag = (address >> (block_offset_bits + set_index_bits)
               ) & ((1 << (32 - block_offset_bits - set_index_bits)) - 1)

        return set_index, tag

    def read_address(self, address):
        """
        Simulates a cache read operation for a given memory address.

        Args:
            address (int): The memory address to read.

        Returns:
            bool: True if the cache hit, False if it's a cache miss.
        """
        self.access_counter += 1
        set_index, tag = self.get_set_index_and_tag(address)
        set_ = self.sets[set_index]

        for line in set_:
            if line.tag == tag:
                line.last_used = self.access_counter
                return True

        self.handle_miss(set_index, tag)
        return False

    def handle_miss(self, set_index, tag):
        """
        Handles cache misses by replacing or initializing cache lines.

        Args:
            set_index (int): The set index where the miss occurred.
            tag (int): The tag of the missed cache line.
        """
        set_ = self.sets[set_index]

        for line in set_:
            if line.last_used == 0:
                line.tag = tag
                line.last_used = self.access_counter
                return

        least_used = min(set_, key=lambda line: line.last_used)
        least_used.tag = tag
        least_used.last_used = self.access_counter

    def print_cache_state(self):
        """
        Prints the current state of the cache.
        """
        for i, set_ in enumerate(self.sets):
            print(
                f"Set {i}: {[f'Tag: {line.tag}, Last Used: {line.last_used}' for line in set_]}")
