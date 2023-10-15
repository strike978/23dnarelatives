import streamlit as st
import pandas as pd
from collections import Counter

def process_csv(file):
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(file)
    
    # Get the unique number of people under the Display Name column
    unique_display_names = df["Display Name"].nunique()
    
    # Filter out rows with NaN values in Maternal Haplogroup and Paternal Haplogroup columns
    filtered_df = df.dropna(subset=["Maternal Haplogroup", "Paternal Haplogroup"])
    
    # Initialize counters for maternal and paternal haplogroups
    maternal_haplogroup_counter = Counter(filtered_df["Maternal Haplogroup"])
    paternal_haplogroup_counter = Counter(filtered_df["Paternal Haplogroup"])
    
    # Sort the haplogroups from most to least frequent
    sorted_maternal_haplogroups = maternal_haplogroup_counter.most_common()
    sorted_paternal_haplogroups = paternal_haplogroup_counter.most_common()
    
    return unique_display_names, sorted_maternal_haplogroups, sorted_paternal_haplogroups

st.title("23andme DNA Relatives Haplogroups Analysis")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    unique_display_names, sorted_maternal_haplogroups, sorted_paternal_haplogroups = process_csv(uploaded_file)

    st.subheader("Analysis Results")
    st.write("Unique number of people:", unique_display_names)

    st.subheader("Most common Maternal Haplogroups:")
    maternal_haplogroups_text = "\n".join([f"{haplogroup}: {count}" for haplogroup, count in sorted_maternal_haplogroups])
    st.code(maternal_haplogroups_text)

    st.subheader("Most common Paternal Haplogroups:")
    paternal_haplogroups_text = "\n".join([f"{haplogroup}: {count}" for haplogroup, count in sorted_paternal_haplogroups])
    st.code(paternal_haplogroups_text)
