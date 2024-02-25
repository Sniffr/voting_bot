import pandas as pd
import requests
from bs4 import BeautifulSoup

# Initialize or load existing data from CSV file
csv_file = 'contacts.csv'
try:
    existing_contacts_df = pd.read_csv(csv_file)
except FileNotFoundError:
    existing_contacts_df = pd.DataFrame(columns=['Name', 'Phone Number', 'Email'])

# Loop to run the scraper 10 times with different seeds
for i in range(40):
    seed = 273 + i  # Update the seed for each iteration
    # Update the URL with the current seed value
    url = f'https://www.random-name-generator.com/south-africa?s={seed}&search_terms=&gender=&search_terms=&n=10'

    print(f'Fetching data from {url} with seed {seed}...')

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the divs that contain the generated data
    generated_data_divs = soup.find_all('div', class_='col-sm-12 mb-3')

    # Prepare a list to store the new data for this seed
    new_contacts = []

    # Loop through each div and extract the names, emails, and phone numbers
    for div in generated_data_divs:
        # Extract name and remove gender in brackets
        name_with_gender = div.find('dd', class_='h4 col-12').text.strip()
        name = ' '.join(name_with_gender.split(' ')[:-1])

        # Extract phone number
        phone_number = div.find('dt', text='Phone Number:').find_next_sibling('dd').text.strip()

        # Extract email
        email = div.find('dt', text='Email:').find_next_sibling('dd').text.strip()

        # Append the data to the list
        new_contacts.append({'Name': name, 'Phone Number': phone_number, 'Email': email})

    # Convert the list to a DataFrame
    new_contacts_df = pd.DataFrame(new_contacts)

    # Check for new names that don't exist in the existing data
    unique_contacts_df = new_contacts_df[~new_contacts_df['Name'].isin(existing_contacts_df['Name'])]

    # Append unique new data to the existing DataFrame
    if not unique_contacts_df.empty:
        existing_contacts_df = pd.concat([existing_contacts_df, unique_contacts_df], ignore_index=True)

# Write the updated DataFrame to the CSV file after all iterations
existing_contacts_df.to_csv(csv_file, index=False)

print(f'Updated data written to {csv_file}. Unique new entries added across all seeds.')
