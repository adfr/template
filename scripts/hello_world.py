#!/usr/bin/env python3
"""
Simple Hello World job for Cloudera AI
"""

import argparse
import logging
from typing import Optional


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
    parser = argparse.ArgumentParser(description="Hello World Job")
    
    parser.add_argument(
        "--name",
        type=str,
        default="World",
        help="Name to greet"
    )
    
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of times to repeat the greeting"
    )
    
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level"
    )
    
    return parser.parse_args()


def hello_world(name: str, repeat: int) -> None:
    """Print hello world message"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Greeting {name} {repeat} time(s)")
    
    for i in range(repeat):
        message = f"Hello, {name}! (#{i+1})"
        print(message)
        logger.debug(f"Printed message: {message}")
    
    logger.info("Greeting completed")


def main() -> None:
    """Main entry point"""
    args = parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Hello World job")
        hello_world(args.name, args.repeat)
        logger.info("Job completed successfully")
    except Exception as e:
        logger.error(f"Error in Hello World job: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main() 