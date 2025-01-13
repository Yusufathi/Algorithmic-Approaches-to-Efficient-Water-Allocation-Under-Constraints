# Water Allocation Algorithms

This project implements and evaluates various algorithms for water allocation problems. The algorithms optimize water distribution among regions, considering factors such as demands, pipeline losses, and constraints. The project also includes performance analysis and visualization tools.

## Project Structure

+ space_analysis.py: Measures space usage for each algorithm
+ time_analysis.py: Measures execution time for each algorithm
+ visualizations.py: Generates graphs and tables for performance analysis logs
+ logs.txt: Execution logs for test cases and algorithms output
+ execution_output.json: JSON containing results and metrics for all test cases
+ line_graph_space_usage.png: Line graph comparing space usage across techniques
+ line_graph_time_usage.png: Line graph comparing time usage across techniques
+ test_case_technique_analysis.csv: CSV summarizing performance metrics for each technique pepers.
+ A Comprehensive Survey of Machine Learning Methodologies with Emphasis in + Water Resources Management.pdf
+ Application of Ford-Fulkerson Algorithm to Maximum.pdf
+ DYNAMIC OPTIMIZATION METHODS_YS.pdf
+ Multisource and multiuser water resources allocation based on genetic algorithm.pdf

+ allocation_technique.py: Base class for all allocation techniques
+ brute_force_allocation.py: Implementation of brute-force allocation
+ ford_fulkerson_allocation.py: Implementation of Ford-Fulkerson allocation
+ genetic_allocation.py: Implementation of genetic algorithm for allocation
+ proportional_allocation.py: Implementation of proportional allocation
+ extensive_conditions_test_cases.json: Comprehensive test cases for edge

+ conditions ford_fulkerson.py: Standalone Ford-Fulkerson implementation with a test case .
+ main.py: Main script to execute algorithms and log results
+ requirements.txt:  Python dependencies required for the project
+ test_cases.json: Standard test cases for the algorithms

## Getting Started

Prerequisites: Ensure you have installed Python 3.10 or higher. Install the required dependencies by running: `pip install -r requirements.txt`

Running the Project:

Execute Algorithms: Run the main script to execute the algorithms on the test cases and generate results: python main.py Results will be saved in the output/ directory and logged in logs/logs.txt.

Generate Visualizations: To generate graphs and tables based on execution results: python analysis/visualizations.py

## Algorithms Implemented

1. Ford-Fulkerson Algorithm:

Optimizes water allocation by modeling the problem as a maximum flow network.
Uses augmenting paths to maximize flow while adhering to pipeline losses and regional demands.

2. Genetic Algorithm:

Uses evolutionary principles such as selection, crossover, and mutation to find near-optimal solutions for water allocation.

3. Brute Force Allocation:

Explores all possible allocations to find the optimal distribution, ensuring fairness and minimal losses.

4. Proportional Allocation:

Allocates water based on a proportional share of total supply relative to regional demands, adjusted for pipeline losses.
Key Features

### Efficiency Metrics

+ Utilization Efficiency
+ Loss Efficiency
+ Fairness Index
+ Overall Efficiency

### Performance Analysis

Execution time and space usage are logged for each algorithm.
Average performance metrics are calculated and visualized.

### Edge Case Handling

Handles scenarios like zero water supply, no demands, and regions with 100% pipeline losses.

### Outputs

JSON Results:

Contains detailed allocations, metrics, and analysis for each algorithm and test case.
Graphs:

Line graphs comparing time and space usage across techniques.
Tables:

CSV summarizing time, space, and metrics for all techniques.

For questions or contributions, please reach out to the project maintainers
