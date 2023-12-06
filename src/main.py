import argparse
from config import CacheConfig
from cache import Cache


def main():
    # Parsing command line arguments
    parser = argparse.ArgumentParser(description='Cache Simulator')
    parser.add_argument('--block_size', type=int,
                        default=32, help='Block size in bytes')
    parser.add_argument('--num_blocks', type=int, default=128,
                        help='Number of blocks in the cache')
    parser.add_argument('--associativity', type=int,
                        default=1, help='Cache associativity')
    parser.add_argument('--replacement_policy', type=str, default='LRU',
                        choices=['LRU', 'Random'], help='Cache replacement policy')
    args = parser.parse_args()

    # Creating cache configuration
    config = CacheConfig(args.block_size, args.num_blocks,
                         args.associativity, args.replacement_policy)

    # Initializing cache
    cache = Cache(config)

    # TODO: Load addresses and simulate cache operations
    # ...


if __name__ == '__main__':
    main()
