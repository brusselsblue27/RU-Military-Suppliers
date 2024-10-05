import os
from src.OpenSanctionsv2 import run_opensanctions  # OpenSanctions script
from src.cleaningscriptv2 import run_cleaning      # Cleaning script
from src.clearspendingv5 import run_clearspending  # ClearSpending script
from src.datamerge import run_merge                # Merge script
from src.final_clean import run_final_clean        # Final clean script
from src.translate import run_translation          # Translation script

# Set the default location for the Google Translate API key
GOOGLE_CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "your-google-translate-api-key.json")

def get_api_keys():
    """Prompt the user to enter the necessary API keys."""
    open_sanctions_key = input("Please enter your OpenSanctions API Key: ").strip()

    # Prompt for up to 3 ClearSpending API keys
    clearspending_keys = []
    print("Enter up to 3 ClearSpending API keys (press Enter to skip any):")
    for i in range(3):
        key = input(f"ClearSpending API Key #{i + 1}: ").strip()
        if key:
            clearspending_keys.append(key)
        else:
            break

    return open_sanctions_key, clearspending_keys

def get_keywords_preset():
    """Prompt the user to choose between the 'Military' preset or a custom keyword list."""
    default_military_keywords = [
        'military production', 'weapons manufacture', 'arms industry', 'aerospace',
        'shipbuilding', 'military research', 'tank production', 'aircraft production'
    ]

    print("\nChoose your keyword preset:")
    print("1. Military Preset (default military-related keywords)")
    print("2. Custom Preset (define your own keyword list)")

    while True:
        choice = input("Enter 1 for Military Preset or 2 for Custom Preset: ").strip()
        if choice == '1':
            print("\nYou selected the Military Preset.")
            additional_keywords = []
            while True:
                keyword = input("Enter an additional keyword (or press Enter to finish): ").strip()
                if keyword:
                    additional_keywords.append(keyword)
                else:
                    break
            return default_military_keywords + additional_keywords
        elif choice == '2':
            print("\nYou selected the Custom Preset.")
            custom_keywords = []
            while True:
                keyword = input("Enter a custom keyword (or press Enter to finish): ").strip()
                if keyword:
                    custom_keywords.append(keyword)
                else:
                    break
            return custom_keywords
        else:
            print("Invalid choice. Please enter 1 or 2.")

def check_file_exists(filepath):
    """Check if a file exists before proceeding to the next step."""
    if os.path.exists(filepath):
        print(f"File {filepath} exists. Proceeding...")
        return True
    else:
        print(f"Error: File {filepath} does not exist.")
        return False

def main():
    # Get API keys from user input
    sanctions_api_key, clearspending_api_keys = get_api_keys()

    # Get keywords preset from user input
    keywords = get_keywords_preset()

    # Get current working directory (where the script is run)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Output directory should be relative to the current directory
    output_dir = os.path.join(current_dir, "output")
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Step 1: Run OpenSanctions script to generate the first CSV file
    opensanctions_output = os.path.join(output_dir, "sanctioned_entities_with_inn.csv")
    print(f"Running OpenSanctions script... Output will be saved to: {opensanctions_output}")
    run_opensanctions(sanctions_api_key, opensanctions_output, keywords)
    
    # Check if the OpenSanctions output file was created before proceeding
    if not check_file_exists(opensanctions_output):
        print("OpenSanctions script did not create the output file. Please check the API key or script.")
        return  # Exit if the file is not created
    
    # Step 2: Run cleaning script after OpenSanctions output is ready
    cleaned_output = os.path.join(output_dir, "data_cleaned_finalv2.csv")
    print(f"Running cleaning script... Reading from: {opensanctions_output}, Output to: {cleaned_output}")
    run_cleaning(opensanctions_output, cleaned_output)
    
    # Check if the cleaning output file was created before proceeding
    if not check_file_exists(cleaned_output):
        return  # Exit if the file is not created
    
    # Step 3: Run ClearSpending script after cleaning
    spending_output = os.path.join(output_dir, "top_3_suppliers_by_companyv2.csv")
    print(f"Running ClearSpending script... Output to: {spending_output}")
    run_clearspending(cleaned_output, spending_output, clearspending_api_keys)
    
    # Check if the ClearSpending output file was created before proceeding
    if not check_file_exists(spending_output):
        return  # Exit if the file is not created
    
    # Step 4: Run merging script after ClearSpending data is ready
    merge_output = os.path.join(output_dir, "forImportGenius.csv")
    print(f"Running merging script... Output to: {merge_output}")
    run_merge(cleaned_output, spending_output, merge_output)
    
    # Check if the merge output file was created before proceeding
    if not check_file_exists(merge_output):
        return  # Exit if the file is not created
    
    # Step 5: Run final cleaning script after merging
    final_output = os.path.join(output_dir, "forImportGenius_no_duplicates.csv")
    print(f"Running final cleaning script... Output to: {final_output}")
    run_final_clean(merge_output, final_output)
    
    # Check if the final cleaned output file was created before proceeding
    if not check_file_exists(final_output):
        return  # Exit if the file is not created
    
    # Step 6: Run translation script as the last step
    translated_output = os.path.join(output_dir, "data_request.csv")
    print(f"Running translation script... Output to: {translated_output}")
    run_translation(final_output, translated_output, GOOGLE_CREDENTIALS_FILE)

    print("All steps completed successfully.")

if __name__ == "__main__":
    main()
