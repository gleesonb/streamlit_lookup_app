import streamlit as st
import pandas as pd
import csv

# Load the CSV file
@st.cache_data
def load_data():
    # For this example, we'll create a sample DataFrame. In practice, you'd load your actual CSV file.
    return pd.DataFrame({'Name': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Emily Brown']})

# Initialize session state
if 'checked_names' not in st.session_state:
    st.session_state.checked_names = set()

@st.cache_data
def load_data():
    return pd.read_csv('your_names_file.csv')

st.title('Name Lookup App')

# User input
name = st.text_input('Enter a name to look up:')

if name:
    if name in df['Name'].values:
        st.success(f'{name} is in the list!')
        if st.button('Check off'):
            st.session_state.checked_names.add(name)
            st.success(f'{name} has been checked off.')
    else:
        st.error(f'{name} is not in the list.')

# Display checked names
st.subheader('Checked Names:')
for checked_name in st.session_state.checked_names:
    st.write(checked_name)

# Save checked names to a file
if st.button('Save Checked Names'):
    with open('checked_names.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Checked Names'])
        for name in st.session_state.checked_names:
            writer.writerow([name])
    st.success('Checked names saved to checked_names.csv')