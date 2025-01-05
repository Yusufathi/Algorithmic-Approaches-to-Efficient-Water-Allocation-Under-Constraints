import time
import logging

def measure_execution_time(technique, test_case, weights):
    """
    Measure the execution time of an allocation technique for a single test case.

    Args:
        technique: The allocation technique class instance.
        test_case (dict): The test case containing water_supply, demands, pipeline_losses.
        weights (list): The weights for efficiency metrics.

    Returns:
        tuple: (output, execution_time)
    """
    start_time = time.time()
    output = technique.allocate(
        test_case["water_supply"],
        test_case["demands"],
        test_case["pipeline_losses"],
        weights
    )
    execution_time = time.time() - start_time
    return output, execution_time

def log_execution_times(results, average_times):
    """
    Log the execution time of each algorithm for each test case and the average times.

    Args:
        results (list): List of execution times for each test case.
        average_times (dict): Average execution times for each technique.
    """
    logging.info("Time Analysis Start")
    for result in results:
        logging.info(f"Test Case: {result['test_case']}")
        for technique_result in result["results"]:
            logging.info(f"  Technique: {technique_result['technique']}")
            logging.info(f"  Execution Time: {technique_result['execution_time']:.4f} seconds")
        logging.info("-" * 50)

    logging.info("Average Execution Times")
    for technique, avg_time in average_times.items():
        logging.info(f"  Technique: {technique}, Average Time: {avg_time:.4f} seconds")
    logging.info("Time Analysis End")
