import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_execution_output(file_path):
    """
    Load the execution output JSON file.

    Args:
        file_path (str): Path to the execution_output.json file.

    Returns:
        dict: Parsed JSON data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Execution output file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        return json.load(file)


def generate_test_case_techinque_table_csv(data, output_dir):
    """
    Generates a CSV where the rows represent each test case, and the columns
    contain technique names separated into two columns: time and space.

    Args:
        data (dict): The execution output data.
        output_dir (str): Directory to save the output CSV file.
    """
    print("Generating test case technique table...")  # Debugging

    # Initialize the results dictionary
    results = {"Test Case": []}

    # Iterate over test cases and techniques
    for test_case in data["execution_results"]:
        test_case_name = test_case["test_case"]
        results["Test Case"].append(test_case_name)

        for technique in test_case["techniques"]:
            technique_name = technique["technique"]
            time_key = f"{technique_name} Time (s)"
            space_key = f"{technique_name} Space (MB)"

            # Add columns for each technique if not already present
            if time_key not in results:
                results[time_key] = []
            if space_key not in results:
                results[space_key] = []

            # Append time and space for the technique
            results[time_key].append(technique["analysis"]["time"])
            results[space_key].append(technique["analysis"]["space"])

    # Convert the results dictionary to a DataFrame
    df = pd.DataFrame(results)
    print("DataFrame created:\n", df.head())  # Debugging

    # Save the DataFrame to a CSV file
    output_file = os.path.join(output_dir, "test_case_technique_analysis.csv")
    print(f"Saving CSV to {output_file}...")  # Debugging
    df.to_csv(output_file, index=False)
    print("CSV saved successfully!")  # Debugging

def generate_line_graph_time(data, output_dir):
    """
    Generates a line graph for time usage across test cases for each technique.

    Args:
        data (dict): The execution output data.
        output_dir (str): Directory to save the output graph.
    """
    print("Generating line graph for time usage...")  # Debugging

    # Prepare the data for plotting
    techniques_data = {}
    test_case_names = []

    for test_case in data["execution_results"]:
        test_case_name = test_case["test_case"]
        test_case_names.append(test_case_name)
        for technique in test_case["techniques"]:
            technique_name = technique["technique"]
            if technique_name not in techniques_data:
                techniques_data[technique_name] = []
            techniques_data[technique_name].append(technique["analysis"]["time"])

    # Create a DataFrame for the data
    df = pd.DataFrame(techniques_data, index=test_case_names)

    # Plot the line graph
    plt.figure(figsize=(12, 6))
    for technique in df.columns:
        plt.plot(df.index, df[technique], marker='o', label=technique)

    plt.title("Time Usage Across Test Cases")
    plt.xlabel("Test Case")
    plt.ylabel("Time Usage (s)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Technique")
    plt.tight_layout()

    # Save the graph
    output_file = os.path.join(output_dir, "line_graph_time_usage.png")
    plt.savefig(output_file)
    print(f"Time usage line graph saved to {output_file}")  # Debugging
    plt.close()

def generate_line_graph_space(data, output_dir):
    """
    Generates a line graph for space usage across test cases for each technique.

    Args:
        data (dict): The execution output data.
        output_dir (str): Directory to save the output graph.
    """
    print("Generating line graph for space usage...")  # Debugging

    # Prepare the data for plotting
    techniques_data = {}
    test_case_names = []

    for test_case in data["execution_results"]:
        test_case_name = test_case["test_case"]
        test_case_names.append(test_case_name)
        for technique in test_case["techniques"]:
            technique_name = technique["technique"]
            if technique_name not in techniques_data:
                techniques_data[technique_name] = []
            techniques_data[technique_name].append(technique["analysis"]["space"])

    # Create a DataFrame for the data
    df = pd.DataFrame(techniques_data, index=test_case_names)

    # Plot the line graph
    plt.figure(figsize=(12, 6))
    for technique in df.columns:
        plt.plot(df.index, df[technique], marker='o', label=technique)

    plt.title("Space Usage Across Test Cases")
    plt.xlabel("Test Case")
    plt.ylabel("Space Usage (MB)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Technique")
    plt.tight_layout()

    # Save the graph
    output_file = os.path.join(output_dir, "line_graph_space_usage.png")
    plt.savefig(output_file)
    print(f"Space usage line graph saved to {output_file}")  # Debugging
    plt.close()

def main():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    execution_output_file = os.path.join(current_dir, "../output/execution_output.json")
    output_dir = os.path.join(current_dir, "../output")


    # Directory to save visualizations
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    # Load the execution output data
    execution_data = load_execution_output(execution_output_file)
    
    #Generate Visualizations
    generate_test_case_techinque_table_csv(execution_data, output_dir)
    generate_line_graph_time(execution_data, output_dir)
    generate_line_graph_space(execution_data, output_dir)


    


if __name__ == "__main__":
    main()
