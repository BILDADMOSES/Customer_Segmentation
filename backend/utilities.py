import pandas as pd

def convert_xls_to_csv(xls_file_path, csv_file_path):
    # Read the XLS file using pandas
    df = pd.read_excel(xls_file_path, engine="xlrd")

    # Convert the pandas DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)


def convert_headers(old_headers, to_camel_case=True):
    new_headers = []
    for header in old_headers:
        if to_camel_case:
            words = header.split('_')
            new_header = words[0] + ''.join(word.capitalize() for word in words[1:])
        else:
            words = header.split('_')
            new_header = '_'.join([word.lower() if i == 0 else word.capitalize() for i, word in enumerate(words)])
            new_header = 'customer_' + new_header if '_' not in header else new_header

        new_headers.append(new_header)

    return new_headers
