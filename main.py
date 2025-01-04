import os
import json
from techniques.ford_fulkerson_allocation import FordFulkersonAllocation
from techniques.dynamic_allocation import DynamicProgrammingAllocation
from techniques.brute_force_allocation import BruteForceAllocation
from techniques.genetic_allocation import GeneticAlgorithmAllocation

# Modify this for the technique you want to be tested. 
# for example, if you want to use only the greedy allocation technique, comment the other approaches.
techniques = [
    # FordFulkersonAllocation()
    # DynamicProgrammingAllocation(),
    BruteForceAllocation()
    # GeneticAlgorithmAllocation()
]

# Overall_Efficiency = (w1 * Utilization_Efficiency) + (w2 * Loss_Efficiency) + (w3 * Fairness_Index) 
# Effiency Metrics
weights = [
    0.35, # Utilization Efficiency
    0.35, # Loss Efficiency
    0.30  # Fairness Index
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
                test_case["pipeline_losses"],
                weights
            )
            case_results["results"].append({
                "technique": technique.__class__.__name__,
                "output": output,
                "match_expected": output == test_case["expected_output"]
            })
        results.append(case_results)
    return results

def main():
    test_cases_file = "./test_cases.json" 
    test_cases = read_test_cases(test_cases_file)
    
    results = test_techniques(test_cases, techniques)

    for result in results:
        print(f"Test Case: {result['test_case']}")
        for technique_result in result["results"]:
            test_case = test_cases[results.index(result)]
            output = technique_result["output"]
            demand = test_case["demands"]

            metrics = {k: v for k, v in output.items() if k in ["util", "loss", "fairness", "overall"]}
            allocation = {k: v for k, v in output.items() if k not in metrics}

            print(f"  Technique: {technique_result['technique']}")
            print(f"  Water Supply: {test_case['water_supply']}")
            print(f"  Demands: {demand}")
            print(f"  Pipeline Losses: {test_case['pipeline_losses']}")
            # print(f"  Expected Output: {test_case['expected_output']}")
            print(f"  Output: {allocation}")

            
            loss_ratios = {}
            for region, demand_value in demand.items():
                output_value = allocation.get(region, 0)
                if demand_value > 0:
                    loss_ratios[region] = round(output_value / demand_value, 2)
                else:
                    loss_ratios[region] = None

            print(f"  Supplied Ratio: {loss_ratios}")
            print(f"  Metrics: {metrics}")
            print("-" * 100)




if __name__ == "__main__":
    main()

