import math
import random


class CacheLine:
    def __init__(self, tag=None, data=None):
        self.tag = tag
        self.data = data
        self.last_used = 0  # For LRU


class Cache:
    def __init__(self, config):
        self.config = config
        self.sets = [[CacheLine() for _ in range(config.associativity)]
                     for _ in range(config.num_sets)]
        self.access_counter = 0  # Used for LRU tracking

    def get_set_index_and_tag(self, address):
        block_offset_bits = int(math.log2(self.config.block_size))
        set_index_bits = int(math.log2(self.config.num_sets))
        tag_bits = 32 - block_offset_bits - set_index_bits

        set_index = (address >> block_offset_bits) & (
            (1 << set_index_bits) - 1)
        tag = address >> (block_offset_bits + set_index_bits)
        return set_index, tag

    def read_address(self, address):
        self.access_counter += 1
        set_index, tag = self.get_set_index_and_tag(address)
        set_ = self.sets[set_index]

        for line in set_:
            if line.tag == tag:
                line.last_used = self.access_counter
                print(
                    f"Cache Hit! Address: {hex(address)}, Set Index: {set_index}, Tag: {tag}, Last Used: {line.last_used}")
                return True

        print(
            f"Cache Miss! Address: {hex(address)}, Set Index: {set_index}, Tag: {tag}")
        self.handle_miss(set_index, tag)
        return False

    def handle_miss(self, set_index, tag):
        set_ = self.sets[set_index]

        # Check for an uninitialized line (last_used = 0) in the set
        for line in set_:
            if line.last_used == 0:
                line.tag = tag
                line.last_used = self.access_counter
                return

        # If all lines are used, find the least recently used line
        least_used = min(set_, key=lambda line: line.last_used)
        least_used.tag = tag
        least_used.last_used = self.access_counter

    def print_cache_state(self):
        for i, set_ in enumerate(self.sets):
            print(
                f"Set {i}: {[f'Tag: {line.tag}, Last Used: {line.last_used}' for line in set_]}")

    # Additional methods, if any...
