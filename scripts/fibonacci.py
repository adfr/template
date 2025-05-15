#!/usr/bin/env python3
"""
Fibonacci sequence generator for Cloudera AI
"""

import os
import argparse
import logging
from typing import List


def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging with the specified level"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Fibonacci Sequence Generator")
    
    parser.add_argument(
        "--n",
        type=int,
        default=10,
        help="Generate Fibonacci sequence up to nth number"
    )
    
    parser.add_argument(
        "--output_file",
        type=str,
        default="fibonacci_result.txt",
        help="Path to save the output"
    )
    
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level"
    )
    
    return parser.parse_args()


def generate_fibonacci(n: int) -> List[int]:
    """Generate Fibonacci sequence up to the nth number"""
    logger = logging.getLogger(__name__)
    logger.info(f"Generating Fibonacci sequence up to {n}")
    
    if n <= 0:
        return []
    
    if n == 1:
        return [0]
    
    if n == 2:
        return [0, 1]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        next_number = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_number)
        logger.debug(f"Fibonacci[{i}] = {next_number}")
    
    return fib_sequence


def save_result(sequence: List[int], output_file: str) -> None:
    """Save the Fibonacci sequence to the output file"""
    logger = logging.getLogger(__name__)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    logger.info(f"Saving Fibonacci sequence to {output_file}")
    
    with open(output_file, "w") as f:
        f.write("Fibonacci Sequence:\n")
        for i, num in enumerate(sequence):
            f.write(f"F({i}) = {num}\n")
    
    logger.info("Fibonacci sequence saved successfully")


def main() -> None:
    """Main entry point"""
    args = parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Fibonacci generator job")
        
        # Generate Fibonacci sequence
        sequence = generate_fibonacci(args.n)
        
        # Print the sequence
        logger.info(f"Fibonacci sequence: {sequence}")
        
        # Save the result
        save_result(sequence, args.output_file)
        
        logger.info("Job completed successfully")
    except Exception as e:
        logger.error(f"Error generating Fibonacci sequence: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main() 