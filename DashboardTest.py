import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Title of the app
st.title("District Data Visualization App")

# Path to folders (assumes the script and district folders are in the same directory)
base_path = os.getcwd()  # Current working directory
district_folders = [f"District {i}" for i in range(1, 8)]

# Check for district folders and list them
available_folders = [folder for folder in district_folders if os.path.exists(os.path.join(base_path, folder))]

if not available_folders:
    st.error("No district folders found in the current directory.")
else:
    # Dropdown for district selection
    selected_district = st.selectbox("Select a District", available_folders)
    folder_path = os.path.join(base_path, selected_district)

    # List CSV files in the selected district folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    if not csv_files:
        st.warning(f"No CSV files found in {selected_district}.")
    else:
        # Dropdown for selecting a CSV file
        selected_file = st.selectbox("Select a CSV File", csv_files)
        file_path = os.path.join(folder_path, selected_file)

        # Load the selected CSV file
        raw_data = pd.read_csv(file_path, header=1)  # Skip the first row
        raw_data.rename(columns={raw_data.columns[0]: "Timestamp"}, inplace=True)

        # Ensure Timestamp is datetime
        raw_data['Timestamp'] = pd.to_datetime(raw_data['Timestamp'], errors='coerce')
        raw_data.dropna(subset=['Timestamp'], inplace=True)  # Remove invalid timestamps

        # Replace "NR" with "none" and keep zeros
        raw_data.replace("NR", "none", inplace=True)
        numeric_columns = raw_data.columns[1:]
        for col in numeric_columns:
            raw_data[col] = pd.to_numeric(raw_data[col], errors='coerce')

        # Aggregate data to one point per day (mean values)
        daily_data = raw_data.set_index('Timestamp').resample('D').mean().reset_index()

        # Merge non-numeric data back into the aggregated dataset
        non_numeric = raw_data.set_index('Timestamp').resample('D').first().reset_index()
        for col in non_numeric.columns:
            if col not in daily_data.columns:
                daily_data[col] = non_numeric[col]

        # Display cleaned and aggregated data
        st.write(f"### Data Preview for {selected_district} - {selected_file}")
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




