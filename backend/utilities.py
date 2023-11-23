import pandas as pd


def convert_xls_to_csv(xls_file_path, csv_file_path):
    """
    Converts an XLS file to a CSV file.

    Parameters:
    - xls_file_path: Path to the XLS file.
    - csv_file_path: Path to the output CSV file.
    """
    # Read the XLS file using pandas
    df = pd.read_excel(xls_file_path, engine="xlrd")

    # Convert the pandas DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)


def convert_headers(old_headers, to_camel_case=True):
    """
    Converts headers to camel case or snake case.

    Parameters:
    - old_headers: List of old headers.
    - to_camel_case: Boolean indicating whether to convert to camel case. If False, converts to snake case.

    Returns:
    - new_headers: List of new headers.
    """
    new_headers = []
    for header in old_headers:
        if to_camel_case:
            words = header.split("_")
            new_header = words[0] + "".join(word.capitalize() for word in words[1:])
        else:
            words = header.split("_")
            new_header = "_".join(
                [
                    word.lower() if i == 0 else word.capitalize()
                    for i, word in enumerate(words)
                ]
            )
            new_header = "customer_" + new_header if "_" not in header else new_header

        new_headers.append(new_header)

    return new_headers


def secure_filename(filename):
    """
    Secures a filename by removing any special characters.

    Parameters:
    - filename: The original filename.

    Returns:
    - The secured filename.
    """
    return "".join(x for x in filename if x.isalnum() or x in ["-", "."])


def check_required_fields(input_data_path, required_fields):
    """
    Checks if a CSV file has all the required fields.

    Parameters:
    - input_data_path: Path to the CSV file.
    - required_fields: List of required field names.

    Returns:
    - missing_fields: List of missing field names.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_data_path)

    # Get the list of field names in the DataFrame
    field_names = df.columns.tolist()

    # Find the required fields that are missing from the DataFrame
    missing_fields = [field for field in required_fields if field not in field_names]

    return missing_fields
