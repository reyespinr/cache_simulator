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
    parser.add_argument('--address_file', type=str,
                        help='Path to the file with memory addresses')
    args = parser.parse_args()

    # Creating cache configuration
    config = CacheConfig(args.block_size, args.num_blocks,
                         args.associativity, args.replacement_policy)

    # Initializing cache
    cache = Cache(config)

    # Variables to track hits and misses
    hits, misses = 0, 0

    # Process the address file
    try:
        with open(args.address_file, 'r') as file:
            for line in file:
                try:
                    # Converting hex string to int
                    address = int(line.strip(), 16)
                    if cache.read_address(address):
                        hits += 1
                    else:
                        misses += 1
                except ValueError:
                    print(f"Invalid address format: {line.strip()}")
    except FileNotFoundError:
        print(f"Address file not found: {args.address_file}")
        return

    # Print the hit/miss rate
    total_accesses = hits + misses
    hit_rate = (hits / total_accesses) * 100 if total_accesses > 0 else 0
    miss_rate = (misses / total_accesses) * 100 if total_accesses > 0 else 0
    cache_size_bytes = args.block_size * args.num_blocks  # Total cache size in bytes
    cache_size_kb = cache_size_bytes / 1024  # Convert bytes to kilobytes
    print(f"Cache size: {cache_size_kb}k")  # Display cache size in kB
    print(f"Reads: {total_accesses}")
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    print(f"Hit Rate: {hit_rate:.2f}%")
    print(f"Miss Rate: {miss_rate:.2f}%")


if __name__ == '__main__':
    main()
