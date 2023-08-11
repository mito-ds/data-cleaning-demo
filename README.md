# Data Cleanliness Verification

**Try the deployed app [here](https://mito-data-cleaning-demo.streamlit.app)**

This Streamlit App allows you to import data, and clean it using the mitosheet library. The app is preconfigured with a set of data checks and prompts you to fix up specific issues in the data.

It ensures the your data has the following properties:
1. The first column is the issue date, and is of type datetime.
2. The issue date column is a datetime column.
3. There are no null values in the issue date column.
4. The Notes column is not included in the dataframe.
5. The term column is an integer.

### Why is this app useful?
This app could be used in the first step of a data engineering pipeline. It allows you, the data engineer, to help data analysts ensure their data conforms to a specific schema before they continue their analysis. 

In this app, only if the user has fixed all of the issues in their data, will they be able to export the data to a csv file. You could update this app to export the data to a database instead.

### Mito Streamlit Package 
Learn more about the Mito Streamlit package [here](https://docs.trymito.io/mito-for-streamlit/getting-started) or following the [getting started guide](https://docs.trymito.io/mito-for-streamlit/create-an-app).

### Run Locally 
1. Create a virtual environment:
```
python3 -m venv venv
```

2. Start the virtual environment:
```
source venv/bin/activate
```

3. Install the required python packages:
```
pip install -r requirements.txt
```

4. Start the streamlit app
```
streamlit run main.py
```
