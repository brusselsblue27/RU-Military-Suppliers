import requests
import pandas as pd

def run_opensanctions(api_key, output_path, additional_keywords=None):
    """Run the OpenSanctions data fetch with user-specified keywords."""
    
    print("Running OpenSanctions with the following output path:", output_path)
    
    # Default keywords for sanctioned companies in Russia
    default_keywords = [
        'military production', 'weapons manufacture', 'arms industry', 'aerospace',
        'shipbuilding', 'military research', 'tank production', 'aircraft production'
    ]

    # Combine default keywords with any additional keywords from the user
    if additional_keywords:
        keywords = default_keywords + additional_keywords
    else:
        keywords = default_keywords

    exclude_keywords = [
        'political', 'bank', 'PMC', 'finance', 'insurance', 'fund', 'investment', 
        'lobbying', 'military organization', 'political groups',
        'media', 'propaganda', 'ministry', 'agency'
    ]

    all_results = []
    batch_size = 100
    more_results = True

    def extract_tax_info(properties):
        tax_info = {'taxNumber': None, 'innCode': None}
        tax_info['taxNumber'] = properties.get('taxNumber', [None])[0]
        tax_info['innCode'] = properties.get('innCode', [None])[0]
        return tax_info

    for keyword in keywords:
        print(f"Searching for keyword: {keyword}")
        offset = 0
        while more_results:
            query_params = {
                'q': keyword,
                'countries': 'RU',  # Focus on Russian companies
                'schema': 'LegalEntity',  # Ensure we're dealing with legal entities
                'topics': 'sanction',  # Include only sanctioned entities
                'fuzzy': 'true',
                'limit': batch_size,
                'offset': offset
            }
            headers = {'Authorization': f'Bearer {api_key}'}
            
            print("Sending request to OpenSanctions API...")
            try:
                response = requests.get('https://api.opensanctions.org/search/sanctions', headers=headers, params=query_params)
                
                # Print the status of the request
                print(f"Response status code: {response.status_code}")
                
                # Check if the request was successful
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    
                    # If no results are returned
                    if not results:
                        print(f"No results found for keyword: {keyword}")
                    
                    # Process each result
                    for result in results:
                        entity_caption = result.get('caption', '').lower()
                        entity_properties = result.get('properties', {})
                        
                        # Skip excluded entities
                        if any(exclude_kw in entity_caption for exclude_kw in exclude_keywords):
                            continue
                        
                        # Extract tax information
                        tax_info = extract_tax_info(entity_properties)
                        result['taxNumber'] = tax_info['taxNumber']
                        result['innCode'] = tax_info['innCode']
                        all_results.append(result)

                    # If the results are less than the batch size, stop pagination
                    if len(results) < batch_size:
                        more_results = False
                    else:
                        offset += batch_size  # Move to the next page of results
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    more_results = False
            except Exception as e:
                print(f"Failed to send request to OpenSanctions API: {e}")
                more_results = False

    # Convert all results into a DataFrame
    if all_results:
        df = pd.DataFrame(all_results)
        
        # Select only the columns of interest
        df_selected = df[['id', 'caption', 'schema', 'taxNumber', 'innCode']]
        
        # Save the results to a CSV file
        try:
            df_selected.to_csv(output_path, index=False)
            print(f"Data saved successfully to {output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
    else:
        print("No results found.")

# The main block for standalone testing (optional)
if __name__ == "__main__":
    # If running standalone, you can still test the script
    api_key = "your_opensanctions_api_key_here"  # Replace this if testing standalone
    output_path = "./sanctioned_entities_with_inn.csv"
    additional_keywords = ['explosives', 'missile', 'drones']
    run_opensanctions(api_key, output_path, additional_keywords)
