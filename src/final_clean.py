import pandas as pd

def run_final_clean(merged_file, output_file):
    """Clean the merged factories and suppliers data."""
    
    # Step 1: Load the merged CSV file
    with open(merged_file, 'r', encoding='utf-8') as f:
        raw_content = f.readlines()

    # Step 2: Parse the raw content, handling "factories" and "suppliers" headers
    factories_data = []
    suppliers_data = []
    current_section = None  # Track which section we're in

    for line in raw_content:
        # Identify the section headers and set the section we're in
        if '**factories**' in line:
            current_section = 'factories'
            continue
        elif '**suppliers**' in line:
            current_section = 'suppliers'
            continue

        # Skip empty lines and column headers
        if 'caption,innCode' in line or line.strip() == "":
            continue

        # Split the line into caption and innCode
        parts = line.strip().split(',')
        if len(parts) == 2:
            caption, inn_code = parts[0].strip(), parts[1].strip()

            # Append the data to the respective section
            if current_section == 'factories':
                factories_data.append([caption, inn_code])
            elif current_section == 'suppliers':
                suppliers_data.append([caption, inn_code])

    # Step 3: Convert both sections to DataFrames
    df_factories = pd.DataFrame(factories_data, columns=['caption', 'innCode'])
    df_suppliers = pd.DataFrame(suppliers_data, columns=['caption', 'innCode'])

    # Step 4: Identify and remove duplicate INNs
    combined_df = pd.concat([df_factories, df_suppliers], ignore_index=True)

    # Remove rows where the 'innCode' is duplicated
    combined_df.drop_duplicates(subset='innCode', inplace=True)

    # Step 5: Write the cleaned data back to a CSV file, maintaining the section headers
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write the factories header
        f.write('**factories**\n')
        f.write('caption,innCode\n')
        
        # Write the cleaned factories data
        df_factories.to_csv(f, header=False, index=False)

        # Add some spacing
        f.write('\n')

        # Write the suppliers header
        f.write('**suppliers**\n')
        f.write('caption,innCode\n')

        # Write the cleaned suppliers data
        df_suppliers.to_csv(f, header=False, index=False)

    print(f"Cleaned file created successfully at {output_file}")
