# OpenSanctions Project

## Overview

The **RU-Military-Suppliers** is a command-line tool that allows users to collect, clean, and translate data related to sanctioned entities, primarily focusing on military-linked companies in Russia. This tool integrates with the **OpenSanctions API**, **ClearSpending API**, and **Google Translate API** to retrieve, process, and analyze information on sanctioned companies and their suppliers.

### Main Features:
1. Retrieve and search sanctioned entities related to military production in Russia from the OpenSanctions database.
2. Clean and process the data for accuracy, removing duplicates and irrelevant records.
3. Query the ClearSpending API to identify suppliers linked to the sanctioned companies.
4. Merge and refine the data into a single dataset, ready for further analysis.
5. Translate the company names into Russian using Google Translate to aid further research and integration.

## Prerequisites: API Keys

To use the OpenSanctions Project, you will need to bring your own API keys from the following services:

1. **OpenSanctions API**:
   - [Sign up for an API key here](https://www.opensanctions.org/docs/api/) to retrieve data from OpenSanctions about sanctioned entities.
     Journalists can receive a free API key when signing up with a work email. This allows for 20,000 calls per month. 
   
2. **ClearSpending API**:
   - The tool supports up to **3 API keys** for the ClearSpending service, which can be used to query contracts and find suppliers.
   - Obtain your ClearSpending API key from [ClearSpending](https://clearspending.ru/about/).
     It is beneficial to make several accounts and generate 2-3 API keys as the API call limits are stingy. RU-Military-Suppliers will automatically toggle between keys when reaching usage limits.
   
3. **Google Translate API**:
   - [Sign up for Google Cloud Translation](https://cloud.google.com/translate/docs/setup) and create a service account with a JSON key file. This will be used to translate the company names.
   - **Important**: Once you have the Google Translate API JSON file, rename it to `your-google-translate-api-key.json` and place it in the top-level directory of this project (the same folder where `main.py` is located).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/OpenSanctionsProject.git
   cd OpenSanctionsProject

