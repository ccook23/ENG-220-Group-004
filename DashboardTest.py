import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("CSV Data Visualization App")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file and clean the header
    raw_data = pd.read_csv(uploaded_file, header=1)  # Skip the first row
    raw_data.rename(columns={raw_data.columns[0]: "Timestamp"}, inplace=True)

    # Ensure Timestamp is datetime
    raw_data['Timestamp'] = pd.to_datetime(raw_data['Timestamp'], errors='coerce')
    raw_data.dropna(subset=['Timestamp'], inplace=True)  # Remove invalid timestamps

    # Replace "NR" with "none" in all columns
    raw_data.replace("NR", "none", inplace=True)

    # Convert numeric columns, keeping zeros
    numeric_columns = raw_data.columns[1:]
    for col in numeric_columns:
        raw_data[col] = pd.to_numeric(raw_data[col], errors='coerce')  # Keeps zeros, converts invalid to NaN

    # Aggregate data to one point per day (mean values)
    daily_data = raw_data.set_index('Timestamp').resample('D').mean().reset_index()

    # Merge non-numeric data back into the aggregated dataset
    non_numeric = raw_data.set_index('Timestamp').resample('D').first().reset_index()
    for col in non_numeric.columns:
        if col not in daily_data.columns:
            daily_data[col] = non_numeric[col]

    # Display cleaned and aggregated data
    st.write("### Data Preview (Daily Aggregated)")
    st.dataframe(daily_data)

    # Dropdown for selecting columns
    columns = daily_data.columns.tolist()
    x_column = st.selectbox("Select X-axis column", columns, index=0)  # Default to "Timestamp"
    y_column = st.selectbox("Select Y-axis column", columns[1:], index=0)  # Skip "Timestamp"

    # Dropdown for graph type
    graph_type = st.selectbox(
        "Select Graph Type",
        ["Line", "Scatter", "Bar"]
    )

    # Plot button
    if st.button("Plot Graph"):
        fig, ax = plt.subplots()

        if graph_type == "Line":
            ax.plot(daily_data[x_column], daily_data[y_column], marker='o')
            ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

        elif graph_type == "Scatter":
            ax.scatter(daily_data[x_column], daily_data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

        elif graph_type == "Bar":
            ax.bar(daily_data[x_column], daily_data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        st.pyplot(fig)

    st.write("Tip: Data has been aggregated to one point per day for better performance.")
else:
    st.info("Please upload a CSV file to get started.")



