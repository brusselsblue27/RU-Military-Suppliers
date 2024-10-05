import time
import requests
import pandas as pd

def run_clearspending(input_file, output_file, api_keys):
    """Processes each company and finds the top suppliers by querying the Clearspending API."""

    # API Keys provided by the user
    current_key_index = 0  # Track the current API key

    def switch_api_key():
        """Switch to the next API key in the list, cycling through them."""
        nonlocal current_key_index
        current_key_index += 1
        if current_key_index >= len(api_keys):
            print("All API keys have reached their quota. Please try again later.")
            raise SystemExit
        print(f"Switching to API Key #{current_key_index + 1}")

    def query_clearspending(inn=None, page_size=50, start_date=None, end_date=None):
        """Queries the Clearspending API by INN to find contracts where they are customers within a time frame."""
        params = {
            'apikey': api_keys[current_key_index],
            'page_size': page_size,
            'sort': '-amount_rur',  # Sort by contract amount in descending order
            'sign_date_gte': start_date,
            'sign_date_lte': end_date,
        }
        try:
            if inn:
                print(f"Searching by Customer INN: {inn}")
                params['customer_inn'] = inn  # Query by customer INN
                response = requests.get(f"https://newapi.clearspending.ru/csinternalapi/v1/filtered-contracts/", params=params)
                
                if response.status_code == 429:  # Handle rate limit exceeded (429)
                    print(f"Rate limit exceeded for API Key #{current_key_index + 1}.")
                    switch_api_key()
                    time.sleep(5)  # Wait before retrying with a new key
                    return query_clearspending(inn, page_size, start_date, end_date)

                if response.status_code == 200:
                    result = response.json()
                    if result.get('count', 0) > 0:
                        return result
                    print("No results found with Customer INN.")
                else:
                    print(f"INN search failed: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error querying the API: {e}")
        return None

    def process_data_and_find_suppliers(data, start_date, end_date):
        """Processes each company and finds the top suppliers by querying the Clearspending API."""
        output_data = []
        for index, row in data.iterrows():
            caption = row['caption']
            print(f"\n--- Searching for company: {caption} (Index {index}) ---")
            inn_code = str(int(row['innCode'])) if not pd.isnull(row['innCode']) else None

            # Query API for contracts where the entity is a customer
            result = query_clearspending(inn=inn_code, start_date=start_date, end_date=end_date)
            if result:
                contracts = result.get('data', [])
                suppliers = {}
                for contract in contracts:
                    for supplier_inn, supplier_name, amount in zip(
                        contract.get('supplier_inns', []),
                        contract.get('supplier_names', []),
                        [contract.get('amount_rur')] * len(contract.get('supplier_inns', []))
                    ):
                        if supplier_inn not in suppliers:
                            suppliers[supplier_inn] = {'name': supplier_name, 'total_value': amount}
                        else:
                            suppliers[supplier_inn]['total_value'] += amount

                # Sort suppliers by total_value and take the top 3
                top_suppliers = sorted(suppliers.items(), key=lambda x: x[1]['total_value'], reverse=True)[:3]

                # Add the top suppliers to the output data
                for supplier_inn, supplier_info in top_suppliers:
                    output_data.append({
                        'Company Name': caption,
                        'Supplier Name': supplier_info['name'],
                        'Supplier INN': supplier_inn,
                        'Total Contract Value': supplier_info['total_value']
                    })
            else:
                print(f"No results found for company: {caption}")

            time.sleep(5)  # Respect a 5-second delay between API requests to avoid overwhelming the API
        return output_data

    # Load the input data
    data = pd.read_csv(input_file)

    # Define the time frame (these can be passed dynamically if needed)
    start_date = '2014-07-31'  # Start of sanctions
    end_date = '2022-02-23'    # Invasion of Ukraine

    # Process the data to find the top 3 suppliers for each company
    output_data = process_data_and_find_suppliers(data, start_date=start_date, end_date=end_date)

    # Save the output data to a CSV file
    output_df = pd.DataFrame(output_data)
    output_df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
