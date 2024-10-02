"""
run_crew.py

This script serves as the entry point for running a crew of AI agents.
It imports the auto_app module and calls its run_agents function with
a command-line argument.

Usage:
    python run_crew.py <path_to_input_file>

The script expects one command-line argument: the path to the input file
that contains the necessary configuration for running the AI agents.
"""

import auto_app
import sys

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python run_crew.py <path_to_input_file>")
        sys.exit(1)

    # Run the agents using the provided input file
    input_file_path = sys.argv[1]
    auto_app.run_agents(input_file_path)