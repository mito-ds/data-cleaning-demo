"""
This is a demo of the mitosheet library. It is a simple streamlit app that allows you to import data and clean it using mitosheet.
"""

import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet


st.title("Data Cleaning Demo")

st.markdown("""
This is a demo of the mitosheet library. It is a simple streamlit app that allows you to import data and clean it using mitosheet, and
demo the flexibility Mito provides when cleaning data. 

In the mitosheet below:
1. Click **Import** > **Import Files** and select an XLSX file from the `data` folder.
2. Click the **Import Button**, and configure the import to skip rows depending on the file you choose.
3. Use the Mitosheet to rename columns to fix up    


""")

mitosheet_import, manual_import = st.tabs(["Mitosheet Import", "Manual Import"])


CHECKS_AND_ERRORS = [
    # First column is issue date
    (
        lambda df: df.columns[0] != 'issue date', 
        'Please edit the first column name to "issue date".',
        'You can do this by double clicking on the column name.'
    ),
    # Correct dtype
    (
        lambda df: df["issue date"].dtype != "datetime64[ns]",
        'Please change the dtype of the "issue date" column to datetime.',
        'You can do this by clicking on the Filter icon, and then selecting from the "dtype" dropdown.'

    ),
    # No null values
    (
        lambda df: df["issue date"].isnull().sum() > 0,
        'Please filter out all null values.',
        'You can do this by clicking the filter icon, and adding an "Is Not Empty" filter.'
    ),
    # Delete the Notes column
    (
        lambda df: "Notes" in df.columns,
        'Please delete the "Notes" column, which is the final column of the dataframe.',
        'You can do this by selecting the column header and pressing the Delete key.'
    ),
    # Turn the term column into a number with the formula =VALUE(LEFT(term, 3))
    (
        lambda df: df["term"].dtype != "int64",
        'Please extract the number of months from the "term" column.',
        'To do so, double click on a cell in the column, and write the formula `=INT(LEFT(term, 3))`.'
    ),
]

def run_data_checks(df):
    for check, error_message, help in CHECKS_AND_ERRORS:
        if check(df):
            st.error(error_message + " " + help)
            return False
    return True

def do_analysis(df):
    st.success("All checks passed! This data is clean, and ready for analysis.")

    # Make a plot of distribution per day
    pass


with mitosheet_import:
    
    st.header("Mitosheet Import")

    # TODO: add import folder
    dfs, _ = spreadsheet()

    # Get the first dataframe
    if len(dfs) > 0:
        df = list(dfs.values())[0]
        check_passed = run_data_checks(df)
        if check_passed:
            do_analysis(df)

with manual_import:

    st.header("Manual Import")

    # Allow users to import from the data folder

    file_path = st.selectbox("Select a file to import", [None, "./data/loans 2010.csv"])

    if file_path:

        df = pd.read_csv(file_path)
        st.dataframe(df)

        st.write("""
Scroll to the bottom of this page to see errors with this data, and then use the inputs below to fix them. The user may need
multiple of these options, but we provide inputs for just the 5 or so most common data cleaning operations.
""")

        # Allow users to select a column, and then rename it
        st.subheader("Rename a column")
        column = st.selectbox("Select a column to rename", df.columns)
        new_name = st.text_input("Enter a new column name")
        if new_name:
            st.success(f"Renamed {column} to {new_name}")
            df = df.rename(columns={column: new_name})

        # Allow users to select a column, and then delete it
        st.subheader("Delete a column")
        column = st.selectbox("Select a column to delete", df.columns)
        if st.button("Delete column"):
            st.success(f"Deleted {column}")
            df = df.drop(columns=[column])

        # Allow users to select a column, and then change the dtype
        st.subheader("Change a column dtype")
        column = st.selectbox("Select a column to change the dtype", df.columns)
        new_dtype = st.selectbox("Select a new dtype", [None, "int64", "float64", "datetime64[ns]", "object"])
        if new_dtype:
            st.success(f"Changed {column} to {new_dtype}")
            df = df.astype({column: new_dtype})

        # Allow users to select a column, and then filter out null values
        st.subheader("Filter out null values")
        column = st.selectbox("Select a column to filter out null values", df.columns)
        if st.button("Filter out null values"):
            st.success(f"Filtered out null values from {column}")
            df = df[df[column].notnull()]
        
        # Allow users to select a column, and then extract a number from it
        st.subheader("Extract a number from a column")
        column = st.selectbox("Select a column to extract a number from", df.columns)
        if st.button("Extract number from column"):
            st.success(f"Extracted number from {column}")
            df[column] = df[column].apply(lambda x: int(x.split()[0]))

        check_passed = run_data_checks(df)
        if check_passed:
            do_analysis(df)

