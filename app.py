import streamlit as st
import pandas as pd
import time

# Define a function to extract unique names from a CSV file
def get_unique_names_from_csv(file):
    df = pd.read_csv(file)
    unique_names = df['Display Name'].unique()
    return unique_names, df  # Return both unique names and the original DataFrame

# Streamlit app
st.set_page_config(layout="wide", page_title="23andme DNA Relatives Filter", page_icon="🧬")
st.header('DNA :green[Relatives Filter]')

st.caption(
    'We do not store your 23andMe DNA Relatives Data on our servers')


# Create a file upload widget
uploaded_file = st.file_uploader("Upload 23andme DNA Relatives Data File", type=["csv"])

# Create a loading spinner for data processing
with st.spinner("Processing data..."):
    if uploaded_file is not None:
        st.write("File uploaded!")

        # Process the uploaded file and obtain unique names and the original DataFrame
        unique_names, df = get_unique_names_from_csv(uploaded_file)


        # Place the filter text inputs on the same row
        col1, col2, col3 = st.columns(3)
        with col1:
            name_filter = st.text_input("Filter by Name:")

        with col2:
            paternal_haplogroup_filter = st.text_input("Filter by Paternal Haplogroup:")

        with col3:
            maternal_haplogroup_filter = st.text_input("Filter by Maternal Haplogroup:")

        # Filter and display data frame
        filtered_names = [name for name in unique_names if 
                          (not name_filter or name_filter.lower() in name.lower()) and
                          (not paternal_haplogroup_filter or 
                           df[(df['Display Name'] == name) & 
                              df['Paternal Haplogroup'].str.contains(paternal_haplogroup_filter, case=False)].shape[0] > 0) and
                          (not maternal_haplogroup_filter or 
                           df[(df['Display Name'] == name) & 
                              df['Maternal Haplogroup'].str.contains(maternal_haplogroup_filter, case=False)].shape[0] > 0)]
        
        if len(filtered_names) == 0:
            st.warning("No matching records found.")
        else:
            # Create a DataFrame to display the unique names and additional columns
            unique_names_df = pd.DataFrame(filtered_names, columns=["Relative"])

            # Add columns for 'Paternal Haplogroup', 'Maternal Haplogroup', and 'Link to Profile Page'
            # and populate them with actual data from the original DataFrame
            unique_names_df["Paternal Haplogroup"] = unique_names_df["Relative"].apply(
                lambda name: df[df['Display Name'] == name]['Paternal Haplogroup'].iloc[0]
            )
            unique_names_df["Maternal Haplogroup"] = unique_names_df["Relative"].apply(
                lambda name: df[df['Display Name'] == name]['Maternal Haplogroup'].iloc[0]
            )
            unique_names_df["Link to Profile Page"] = unique_names_df["Relative"].apply(
                lambda name: df[df['Display Name'] == name]['Link to Profile Page'].iloc[0]
            )

            # Display the data frame
            st.dataframe(unique_names_df,use_container_width=True)
