import streamlit as st
import pandas as pd
import csv
from datetime import datetime
import json

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv('your_names_file.csv')

# Initialize session state
if 'checked_names' not in st.session_state:
    st.session_state.checked_names = {}

# Load checked names from file
def load_checked_names():
    try:
        with open('checked_names.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save checked names to file
def save_checked_names():
    with open('checked_names.json', 'w') as file:
        json.dump(st.session_state.checked_names, file)

# Load data
df = load_data()

# Load previously checked names
st.session_state.checked_names = load_checked_names()

st.title('Name Lookup App')

# User input
name = st.text_input('Enter a name to look up:')

# Sorting options
sort_option = st.selectbox('Sort checked names by:', ['Name', 'Timestamp'])

# Pagination
names_per_page = 10
page_number = st.number_input('Page', min_value=1, value=1)
start_idx = (page_number - 1) * names_per_page

# Real-time lookup
if name:
    matching_names = df[df['Name'].str.contains(name, case=False, na=False)]
    if not matching_names.empty:
        st.success(f'Matching names:')
        for matched_name in matching_names['Name'][start_idx:start_idx+names_per_page]:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(matched_name)
            with col2:
                if matched_name not in st.session_state.checked_names:
                    if st.button('Check', key=f'check_{matched_name}'):
                        st.session_state.checked_names[matched_name] = datetime.now().isoformat()
                        st.success(f'{matched_name} has been checked off.')
                        save_checked_names()
            with col3:
                if matched_name in st.session_state.checked_names:
                    if st.button('Uncheck', key=f'uncheck_{matched_name}'):
                        del st.session_state.checked_names[matched_name]
                        st.success(f'{matched_name} has been unchecked.')
                        save_checked_names()

        total_pages = -(-len(matching_names) // names_per_page)  # Ceiling division
        st.write(f'Page {page_number} of {total_pages}')
    else:
        st.error(f'No names matching "{name}" found in the list.')

# Display checked names
st.subheader('Checked Names:')
checked_names_list = list(st.session_state.checked_names.items())
if sort_option == 'Name':
    checked_names_list.sort(key=lambda x: x[0])
else:
    checked_names_list.sort(key=lambda x: x[1], reverse=True)

for checked_name, timestamp in checked_names_list:
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.write(checked_name)
    with col2:
        st.write(datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    with col3:
        if st.button('Uncheck', key=f'uncheck_list_{checked_name}'):
            del st.session_state.checked_names[checked_name]
            st.success(f'{checked_name} has been unchecked.')
            save_checked_names()

# Save checked names to a file
if st.button('Save Checked Names'):
    with open('checked_names.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Checked Names', 'Timestamp'])
        for name, timestamp in st.session_state.checked_names.items():
            writer.writerow([name, timestamp])
    st.success('Checked names saved to checked_names.csv')