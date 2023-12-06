# Cache Simulator

A Python program that simulates the behavior of a cache memory system using different configurations and replacement policies. This README provides instructions on how to set up and run the simulator, details about each command-line argument, and examples of running the simulator with different configurations.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Arguments](#command-line-arguments)
  - [Examples](#examples)
- [Running Tests](#running-tests)

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/reyespinr/cache_simulator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd cache_simulator
   ```

No further installation is required as the simulator is implemented in Python and does not depend on external libraries.

## Usage

### Command-Line Arguments

The Cache Simulator accepts several command-line arguments to configure the cache system and specify the memory addresses to simulate. Here's a description of each argument:

- `--block_size` (default: 32):
  - Block size in bytes.

- `--num_blocks` (default: 128):
  - Number of blocks in the cache.

- `--associativity` (default: 1):
  - Cache associativity.

- `--replacement_policy` (default: 'LRU', choices: ['LRU', 'Random']):
  - Cache replacement policy.

- `--address_file`:
  - Path to the file with memory addresses to simulate.

### Examples

Here are some examples of how to run the Cache Simulator with different configurations:

1. Run the simulator with a block size of 16 bytes, 256 blocks, associativity of 1, LRU replacement policy, and a specific address file:

   ```bash
   python src/main.py --block_size 16 --num_blocks 256 --associativity 1 --replacement_policy LRU --address_file data/addresses.txt
   ```

   Output:
   ```
   Cache size: 4.0k
   Reads: 10000
   Hits: 61
   Misses: 9939
   Hit Rate: 0.61%
   Miss Rate: 99.39%
   ```

2. Run the simulator with a block size of 256 bytes, 256 blocks, associativity of 1, LRU replacement policy, and a specific address file:

   ```bash
   python src/main.py --block_size 256 --num_blocks 256 --associativity 1 --replacement_policy LRU --address_file data/addresses.txt
   ```

   Output:
   ```
   Cache size: 64.0k
   Reads: 10000
   Hits: 978
   Misses: 9022
   Hit Rate: 9.78%
   Miss Rate: 90.22%
   ```

You can customize the cache configuration by adjusting the command-line arguments as needed.

## Running Tests

To run the tests for the cache simulator, use the following command:

```bash
python3 -m unittest tests/test_cache.py
```

This command will execute the unit tests and display the test results.

That's it! You are now ready to set up, run, and test the Cache Simulator with different configurations.
