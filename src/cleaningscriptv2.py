import pandas as pd
import re

def run_cleaning(input_file, output_file):
    """Clean the CSV data."""
    
    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Step 1: Remove rows where there are duplicate innCodes
    df.drop_duplicates(subset='innCode', inplace=True)

    # Step 2: Remove rows where the 'schema' column has the value 'person'
    df = df[df['schema'].str.lower() != 'person']

    # Step 3: Handle missing innCodes by looking at the taxNumber column
    # Assuming the INN code format is numeric with a length of 10 digits (modify as needed)
    inn_code_pattern = re.compile(r'^\d{10}$')

    def check_inn_format(value):
        """Check if the value matches the INN code format."""
        if pd.isna(value):
            return False
        return bool(inn_code_pattern.match(str(value)))

    # Iterate over rows and fill innCode where it's missing
    for index, row in df.iterrows():
        if pd.isna(row['innCode']):  # If innCode is missing
            tax_number = row['taxNumber']
            if check_inn_format(tax_number):
                df.at[index, 'innCode'] = tax_number  # Move taxNumber to innCode
            else:
                df.at[index, 'innCode'] = None  # Leave blank if format doesn't match

    # Step 4: Drop the taxNumber column
    df.drop(columns=['taxNumber'], inplace=True)

    # Step 5: Save the cleaned dataframe to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
