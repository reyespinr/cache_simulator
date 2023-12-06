class CacheConfig:
    """
    Class for cache configuration settings.

    Attributes:
        block_size (int): The size of a cache block in bytes.
        num_blocks (int): The total number of cache blocks.
        associativity (int): The associativity of the cache.
        replacement_policy (str): The cache replacement policy ('LRU' or 'RANDOM').
        num_sets (int): The calculated number of cache sets based on num_blocks and associativity.

    Methods:
        No methods are defined in this class.
    """

    def __init__(self, block_size, num_blocks, associativity, replacement_policy):
        """
        Initializes a CacheConfig object with the specified parameters.

        Args:
            block_size (int): The size of a cache block in bytes.
            num_blocks (int): The total number of cache blocks.
            associativity (int): The associativity of the cache.
            replacement_policy (str): The cache replacement policy ('LRU' or 'RANDOM').

        Calculated Attributes:
            num_sets (int): The calculated number of cache sets based on num_blocks and associativity.
        """
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.associativity = associativity
        self.replacement_policy = replacement_policy
        self.num_sets = num_blocks // associativity  # Calculate num_sets
