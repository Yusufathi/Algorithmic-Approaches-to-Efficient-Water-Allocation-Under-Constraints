import os
import json
from techniques.greedy_allocation import FordFulkersonAllocation
from techniques.dynamic_allocation import DynamicProgrammingAllocation
from techniques.brute_force_allocation import BruteForceAllocation
from techniques.genetic_allocation import GeneticAlgorithmAllocation


# Modify this for the technique you want to be tested. for example, if you want to use only the greedy allocation technique, comment the other approaches.
techniques = [
    FordFulkersonAllocation()
    # DynamicProgrammingAllocation(),
    # BruteForceAllocation(),
    # GeneticAlgorithmAllocation()
]

def read_test_cases(file_path):
    """
    Reads test cases from a JSON file.

    Args:
        file_path (str): Path to the test cases file.

    Returns:
        list: A list of dictionaries, each containing a test case.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test cases file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        test_cases = json.load(file)
    
    # Debugging: Print parsed test cases
    # print("Parsed Test Cases:", test_cases)
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
    test_cases_file = "./test_cases.json"  # Use JSON file
    test_cases = read_test_cases(test_cases_file)
    
    results = test_techniques(test_cases, techniques)

    for result in results:
        print(f"Test Case: {result['test_case']}")
        for technique_result in result["results"]:
            print(f"  Technique: {technique_result['technique']}")
            print(f"  Water Supply: {test_cases[results.index(result)]['water_supply']}")
            print(f"  Demands: {test_cases[results.index(result)]['demands']}")
            print(f"  Pipeline Losses: {test_cases[results.index(result)]['pipeline_losses']}")
            print(f"  Expected Output: {test_cases[results.index(result)]['expected_output']}")
            print(f"  Output: {technique_result['output']}")
            # print(f"  Match Expected: {technique_result['match_expected']}")
        print("-" * 50)

if __name__ == "__main__":
    main()

