import os
import json
from techniques.greedy_allocation import GreedyAllocation
from techniques.dynamic_allocation import DynamicProgrammingAllocation
from techniques.brute_force_allocation import BruteForceAllocation
from techniques.genetic_allocation import GeneticAlgorithmAllocation


# Modify this for the technique you want to be tested. for example, if you want to use only the greedy allocation technique, comment the other approaches.
techniques = [
    GreedyAllocation(),
    DynamicProgrammingAllocation(),
    BruteForceAllocation(),
    GeneticAlgorithmAllocation()
]

def read_test_cases(file_path):
    """
    Reads test cases from a text file.

    Args:
        file_path (str): Path to the test cases file.

    Returns:
        list: A list of dictionaries, each containing a test case.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test cases file not found: {file_path}")
    
    test_cases = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    current_test_case = {}
    for line in lines:
        line = line.strip()
        if line.startswith("Test Case"):
            if current_test_case:
                test_cases.append(current_test_case)
            current_test_case = {"name": line}
        elif line.startswith("Water Supply"):
            current_test_case["water_supply"] = int(line.split(":")[1].strip())
        elif line.startswith("Demands"):
            try:
                demands = line.split(":")[1].strip()
                current_test_case["demands"] = {k.strip(): int(v.strip()) for k, v in (x.split(":") for x in demands.split(",") if ":" in x)}
            except ValueError:
                raise ValueError(f"Invalid format in 'Demands' line: {line}")
        elif line.startswith("Pipeline Losses"):
            try:
                losses = line.split(":")[1].strip()
                current_test_case["pipeline_losses"] = {k.strip(): float(v.strip('%').strip()) / 100 for k, v in (x.split(":") for x in losses.split(",") if ":" in x)}
            except ValueError:
                raise ValueError(f"Invalid format in 'Pipeline Losses' line: {line}")
        elif line.startswith("Expected Output"):
            try:
                expected_output = line.split(":")[1].strip()
                current_test_case["expected_output"] = {k.strip(): int(v.strip()) for k, v in (x.split(":") for x in expected_output.split(",") if ":" in x)}
            except ValueError:
                raise ValueError(f"Invalid format in 'Expected Output' line: {line}")
    if current_test_case:
        test_cases.append(current_test_case)
    
    return test_cases


def test_techniques(test_cases, techniques):
    results = []
    for test_case in test_cases:
        case_results = {
            "test_case": test_case["name"],
            "results": []
        }
        for technique in techniques:
            output = technique.allocate(
                test_case["water_supply"], 
                test_case["demands"], 
                test_case["pipeline_losses"]
            )
            case_results["results"].append({
                "technique": technique.__class__.__name__,
                "output": output,
                "match_expected": output == test_case["expected_output"]
            })
        results.append(case_results)
    return results

def main():
    test_cases_file = "./test_cases.txt"
    test_cases = read_test_cases(test_cases_file)
    
    results = test_techniques(test_cases, techniques)

    for result in results:
        print(f"Test Case: {result['test_case']}")
        for technique_result in result["results"]:
            print(f"  Technique: {technique_result['technique']}")
            print(f"  Output: {technique_result['output']}")
            print(f"  Match Expected: {technique_result['match_expected']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
