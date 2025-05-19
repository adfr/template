#!/usr/bin/env python3
"""
Simple Hello World job for Cloudera AI
"""

def main():
    name = "World"
    repeat = 1
    
    for i in range(repeat):
        print(f"Hello, {name}! (#{i+1})")

if __name__ == "__main__":
    main()