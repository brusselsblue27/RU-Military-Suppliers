import pandas as pd
from google.cloud import translate_v2 as translate
import os
import html

def run_translation(input_file, output_file, google_credentials):
    """Run the translation process on the specified input file."""
    
    # Set up Google Cloud credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

    # Initialize the Google Cloud Translate client
    translate_client = translate.Client()

    # Step 1: Load the CSV file
    print(f"Reading input file: {input_file}")
    df = pd.read_csv(input_file)

    # Step 2: Translate only the rows A3:A269 (index 2 to 268 in Python)
    def translate_text(text, target_language='ru'):
        """Translates text into the target language using Google Translate."""
        result = translate_client.translate(text, target_language=target_language)
        return html.unescape(result['translatedText'])  # Decode HTML entities

    def is_russian(text):
        """Detect if the text is already in Russian (Cyrillic characters)."""
        return any('а' <= char <= 'я' or 'А' <= char <= 'Я' for char in text)

    # Apply translation to rows 3 to 269 in the first column ('caption' or A)
    for i in range(2, 269):  # Corresponds to A3 to A269 in the file
        company_name = df.iloc[i, 0]  # Access column A (the first column in the CSV)
        
        # Translate if the text is not already in Russian
        if not is_russian(company_name):
            df.iloc[i, 0] = translate_text(company_name)

    # Step 3: Save the translated CSV file
    df.to_csv(output_file, index=False)
    print(f"Translated file saved to: {output_file}")
