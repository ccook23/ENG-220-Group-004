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

    # Display cleaned data
    st.write("### Data Preview")
    st.dataframe(raw_data)

    # Dropdown for selecting columns
    columns = raw_data.columns.tolist()
    x_column = st.selectbox("Select X-axis column", columns, index=0)  # Default to "Timestamp"
    y_column = st.selectbox("Select Y-axis column", columns, index=1)  # Default to second column

    # Dropdown for graph type
    graph_type = st.selectbox(
        "Select Graph Type",
        ["Line", "Scatter", "Bar", "Pie"]
    )

    # Plot button
    if st.button("Plot Graph"):
        fig, ax = plt.subplots()

        if graph_type == "Line":
            ax.plot(raw_data[x_column], raw_data[y_column], marker='o')
            ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

        elif graph_type == "Scatter":
            ax.scatter(raw_data[x_column], raw_data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

        elif graph_type == "Bar":
            ax.bar(raw_data[x_column], raw_data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

        elif graph_type == "Pie":
            if len(raw_data[x_column].unique()) <= 10:  # Limit to 10 unique categories for readability
                plt.pie(
                    raw_data[y_column],
                    labels=raw_data[x_column],
                    autopct='%1.1f%%',
                    startangle=90,
                )
                plt.title(f"{y_column} (Pie Chart)")
            else:
                st.error("Pie chart requires fewer unique categories in the X-axis.")

        if graph_type != "Pie":
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)
        else:
            st.pyplot(plt)

    st.write("Tip: Ensure the selected columns are numeric for meaningful plots.")
else:
    st.info("Please upload a CSV file to get started.")
