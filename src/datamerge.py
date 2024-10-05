import pandas as pd

def run_merge(factories_file, suppliers_file, output_file):
    """Merge factories and suppliers data into one CSV file."""

    # Load the two CSV files
    df_factories = pd.read_csv(factories_file)
    df_suppliers = pd.read_csv(suppliers_file)

    # Step 1: Prepare the supplier data for merging
    df_suppliers_selected = df_suppliers[['Supplier Name', 'Supplier INN']].copy()
    df_suppliers_selected.rename(columns={'Supplier Name': 'caption', 'Supplier INN': 'innCode'}, inplace=True)

    # Step 2: Remove unnecessary columns from the factories data
    df_factories.drop(columns=['schema'], inplace=True, errors='ignore')
    df_factories.drop(columns=['id'], inplace=True, errors='ignore')

    # Step 3: Write the merged output to the specified file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        # Write the 'factories' header
        f.write('**factories**\n')
        f.write(','.join(df_factories.columns) + '\n')
        
        for row in df_factories.to_dict(orient='records'):
            f.write(','.join([str(row[col]) for col in df_factories.columns]) + '\n')

        # Add a newline and 'suppliers' header
        f.write('\n**suppliers**\n')
        f.write(','.join(df_factories.columns) + '\n')
        
        for row in df_suppliers_selected.to_dict(orient='records'):
            f.write(','.join([str(row[col]) for col in df_suppliers_selected.columns]) + '\n')

    print(f"Merged file created successfully at {output_file}")
