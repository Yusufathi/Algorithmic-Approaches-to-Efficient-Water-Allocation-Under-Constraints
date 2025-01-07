import os
import json
import logging
from datetime import datetime
from analysis.time_analysis import measure_execution_time
from analysis.space_analysis import measure_memory_usage
from techniques.ford_fulkerson_allocation import FordFulkersonAllocation
from techniques.proportional_allocation import ProportionalAllocation
from techniques.brute_force_allocation import BruteForceAllocation
from techniques.genetic_allocation import GeneticAlgorithmAllocation

# Configure logging
log_file_path = "./logs/logs.txt"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Modify this for the techniques to be tested.
techniques = [
    FordFulkersonAllocation(),
    ProportionalAllocation(),
    BruteForceAllocation(),
    GeneticAlgorithmAllocation()
]

# Efficiency Metrics Weights
weights = [
    0.35,  # Utilization Efficiency
    0.35,  # Loss Efficiency
    0.30   # Fairness Index
]

def read_test_cases(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test cases file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        test_cases = json.load(file)
    
    return test_cases

def test_techniques(test_cases, techniques):
    results = []
    execution_times = {tech.__class__.__name__: [] for tech in techniques}
    memory_usage = {tech.__class__.__name__: [] for tech in techniques}

    output_data = {"execution_results": []}

    logging.info("Execution Start")
    for test_case in test_cases:
        logging.info(f"Test Case: {test_case['name']}")
        case_result = {"test_case": test_case["name"], "techniques": []}
        for technique in techniques:
            # Measure time and space for each technique
            output, execution_time = measure_execution_time(technique, test_case, weights)
            _, peak_memory = measure_memory_usage(technique, test_case, weights)

            # Prepare metrics and allocation
            demand = test_case["demands"]
            metrics = {k: v for k, v in output.items() if k in ["util", "loss", "fairness", "overall"]}
            allocation = {k: v for k, v in output.items() if k not in metrics}

            loss_ratios = {}
            for region, demand_value in demand.items():
                output_value = allocation.get(region, 0)
                if demand_value > 0:
                    loss_ratios[region] = round(output_value / demand_value, 2)
                else:
                    loss_ratios[region] = None

            # Log details
            logging.info(f"  Technique: {technique.__class__.__name__}")
            logging.info(f"  Water Supply: {test_case['water_supply']}")
            logging.info(f"  Demands: {demand}")
            logging.info(f"  Pipeline Losses: {test_case['pipeline_losses']}")
            logging.info(f"  Output: {allocation}")
            logging.info(f"  Supplied Ratio: {loss_ratios}")
            logging.info(f"  Metrics: {metrics}")
            logging.info(f"  Analysis: {{'Time': {execution_time:.4f} Seconds, 'Space': {peak_memory:.4f} MB}}")
            logging.info("-" * 100)

            # Store in results for JSON
            case_result["techniques"].append({
                "technique": technique.__class__.__name__,
                "output": allocation,
                "metrics": metrics,
                "supplied_ratio": loss_ratios,
                "analysis": {"time": round(execution_time, 4), "space": round(peak_memory, 4)}
            })

            # Store metrics for averaging
            execution_times[technique.__class__.__name__].append(execution_time)
            memory_usage[technique.__class__.__name__].append(peak_memory)

        output_data["execution_results"].append(case_result)

    # Calculate averages
    averages = []
    logging.info("Average Time and Space Analysis")
    for technique in techniques:
        avg_time = sum(execution_times[technique.__class__.__name__]) / len(execution_times[technique.__class__.__name__])
        avg_space = sum(memory_usage[technique.__class__.__name__]) / len(memory_usage[technique.__class__.__name__])
        logging.info(f"Technique: {technique.__class__.__name__} --- Average Time: {avg_time:.4f} Seconds --- Average Space: {avg_space:.4f} MB")
        averages.append({
            "technique": technique.__class__.__name__,
            "average_time": round(avg_time, 4),
            "average_space": round(avg_space, 4)
        })
    output_data["averages"] = averages
    logging.info("Execution End")
    logging.info("+" * 100)

    # Save to JSON
    output_file = "./output/execution_output.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=4)

def main():
    test_cases_file = "./test_cases.json"
    test_cases = read_test_cases(test_cases_file)
    test_techniques(test_cases, techniques)

if __name__ == "__main__":
    main()
