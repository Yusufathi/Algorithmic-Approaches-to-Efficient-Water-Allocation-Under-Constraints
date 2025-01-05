import tracemalloc
import logging

def measure_memory_usage(technique, test_case, weights):
    """
    Measure the memory usage of an allocation technique for a single test case.

    Args:
        technique: The allocation technique class instance.
        test_case (dict): The test case containing water_supply, demands, pipeline_losses.
        weights (list): The weights for efficiency metrics.

    Returns:
        tuple: (output, peak_memory)
    """
    tracemalloc.start()
    output = technique.allocate(
        test_case["water_supply"],
        test_case["demands"],
        test_case["pipeline_losses"],
        weights
    )
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return output, peak / (1024 * 1024)  # Convert to MB

def log_memory_usage(results, average_memory):
    """
    Log the memory usage of each algorithm for each test case and the average memory usage.

    Args:
        results (list): List of memory usage for each test case.
        average_memory (dict): Average memory usage for each technique.
    """
    logging.info("Memory Analysis Start")
    for result in results:
        logging.info(f"Test Case: {result['test_case']}")
        for technique_result in result["results"]:
            logging.info(f"  Technique: {technique_result['technique']}")
            logging.info(f"  Peak Memory Usage: {technique_result['peak_memory']:.4f} MB")
        logging.info("-" * 50)

    logging.info("Average Memory Usage")
    for technique, avg_memory in average_memory.items():
        logging.info(f"  Technique: {technique}, Average Memory: {avg_memory:.4f} MB")
    logging.info("Memory Analysis End")
