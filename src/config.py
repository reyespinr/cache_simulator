class CacheConfig:
    def __init__(self, block_size, num_blocks, associativity, replacement_policy):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.associativity = associativity
        self.replacement_policy = replacement_policy
        self.num_sets = num_blocks // associativity  # Calculate num_sets
