import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("Glimpse into Your Insights")

def delete_columns(df, columns_to_delete):
    df = df.drop(columns=columns_to_delete, errors="ignore")
    return df

# Function to create a histogram
def create_histogram(data_frame, column_names):
    for col_name in column_names:
        plt.figure(figsize=(6, 5))
        plt.hist(data_frame[col_name], bins=20, color="skyblue", edgecolor="black")
        plt.title(f"Histogram of {col_name}")
        plt.xlabel(col_name)
        plt.ylabel("Frequency")
        st.pyplot(plt)


def create_line_chart(data, x_col, y_col):
    plt.figure(figsize=(10, 6))
    plt.plot(data[x_col], data[y_col], marker="o", linestyle="-", color="b")
    plt.title(f"Line Chart:{y_col} vs {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    return plt


# Function to create a box plot
def create_box_plot(data_frame, column_name):
    plt.figure(figsize=(8, 6))
    plt.boxplot(data_frame[column_name])
    plt.title(f"Box Plot of {column_name}")
    plt.ylabel(column_name)
    return plt


# Function to create a bar chart
def create_bar_chart(data_frame, x_column, y_column):
    plt.figure(figsize=(8, 6))
    plt.bar(data_frame[x_column], data_frame[y_column], color="skyblue")
    plt.title(f"Bar Chart: {y_column} vs. {x_column}")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.xticks(rotation=45)
    return plt


# Function to create a scatter plot
def create_scatter_plot(data_frame, x_column, y_column):
    plt.figure(figsize=(8, 6))
    plt.scatter(data_frame[x_column], data_frame[y_column], c="skyblue", marker="o")
    plt.title(f"Scatter Plot: {y_column} vs. {x_column}")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    return plt


# Function to create a pie chart
def create_pie_chart(data_frame, column_name):
    plt.figure(figsize=(8, 6))
    counts = data_frame[column_name].value_counts()
    plt.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=["skyblue", "lightcoral", "lightgreen"],
    )
    plt.title(f"Pie Chart: {column_name}")
    return plt


# Function to create a 3D scatter plot
def create_3d_scatter_plot(data_frame, x_column, y_column, z_column):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        data_frame[x_column],
        data_frame[y_column],
        data_frame[z_column],
        c="skyblue",
        marker="o",
    )
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_zlabel(z_column)
    ax.set_title(f"3D Scatter Plot: {x_column}, {y_column}, {z_column}")
    return plt


# Function to create a 3D line plot
def create_3d_line_plot(data_frame, x_column, y_column, z_column):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(
        data_frame[x_column],
        data_frame[y_column],
        data_frame[z_column],
        label="3D Line",
        color="b",
    )
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_zlabel(z_column)
    ax.set_title(f"3D Line Plot: {x_column}, {y_column}, {z_column}")
    return plt


# Upload a CSV file
uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    # Read the file into a DataFrame
    # df = pd.read_csv(uploaded_file)
    df = (
        pd.read_excel(uploaded_file)
        if file_ext == "xlsx"
        else pd.read_csv(uploaded_file)
    )

    all_columns = df.columns.to_list()

    # Basic statistics
    st.subheader("Basic Statistics:")
    st.write("Number of rows:", df.shape[0])
    st.write("Number of columns:", df.shape[1])
    st.write("Column names:", all_columns)
    st.write("Summary statistics:", df.describe())
    st.write("Data Types of Each Column:", df.dtypes)

    columns_with_missing_values = df.columns[df.isna().any()].tolist()

    if columns_with_missing_values:
        st.subheader("Columns with Missing Values:")
        st.write(columns_with_missing_values)

        for column in columns_with_missing_values:
            st.subheader("Select Replacement Method")
            replacement_method = st.selectbox(
                "Methods:",
                [
                    "No Replacement",
                    "Replace_custom",
                ],
                key=f"replacement_method_selectbox_{column}",
            )
            
            if replacement_method == "Replace_custom":
                custom_value = st.text_input("Enter a value to replace nulls:", "NULL")
                df[column].fillna(custom_value)
        st.subheader("Data with Missing Values Handled:")
        st.write(df)
    else:
        st.subheader("No Columns with Missing Values")

    


    # other visualisationas
    st.subheader("Visualisations")
    visualizations = st.multiselect(
        "Select Visualizations",
        [
            "Histogram",
            "Box Plot",
            "Bar Chart",
            "Scatter Plot",
            "Line Chart",
            "Pie Chart",
            "3D Scatter Plot",
            "3D Line Plot",
        ],
    )

    # Generate selected visualizations
    for viz in visualizations:
        if viz == "Histogram":
            col_names = st.multiselect("Select a columns for the Histogram", df.columns)
            create_histogram(df, col_names)
        elif viz == "Box Plot":
            col_name = st.selectbox(
                "Select a column for the Box Plot", df.columns, key="uniquekey_box_plot"
            )
            st.pyplot(create_box_plot(df, col_name))
        elif viz == "Bar Chart":
            x_col = st.selectbox(
                "Select a column for the X-axis", df.columns, key="uniquekey_x_barchart"
            )
            y_col = st.selectbox(
                "Select a column for the Y-axis", df.columns, key="uniquekey_y_barchart"
            )
            st.pyplot(create_bar_chart(df, x_col, y_col))
        elif viz == "Scatter Plot":
            x_col = st.selectbox(
                "Select a column for the X-axis",
                df.columns,
                key="uniquekey_x_scatterplot",
            )
            y_col = st.selectbox(
                "Select a column for the Y-axis",
                df.columns,
                key="uniquekey_y_scatterplot",
            )
            st.pyplot(create_scatter_plot(df, x_col, y_col))
        elif viz == "Line Chart":
            x_col = st.selectbox(
                "Select a column for the X-axis",
                df.columns,
                key="uniquekey_x_linechart",
            )
            y_col = st.selectbox(
                "Select a column for the Y-axis",
                df.columns,
                key="uniquekey_y_linechart",
            )
            st.pyplot(create_line_chart(df, x_col, y_col))
        elif viz == "Pie Chart":
            col_name = st.selectbox(
                "Select a column for the Pie Chart",
                df.columns,
                key="uniquekey_piechart",
            )
            st.pyplot(create_pie_chart(df, col_name))
        elif viz == "3D Scatter Plot":
            x_col = st.selectbox(
                "Select a column for the X-axis",
                df.columns,
                key="uniquekey_x_3D_scatter",
            )
            y_col = st.selectbox(
                "Select a column for the Y-axis",
                df.columns,
                key="uniquekey_y_3D_scatter",
            )
            z_col = st.selectbox(
                "Select a column for the Z-axis",
                df.columns,
                key="uniquekey_z_3D_scatter",
            )
            st.pyplot(create_3d_scatter_plot(df, x_col, y_col, z_col))
        elif viz == "3D Line Plot":
            x_col = st.selectbox(
                "Select a column for the X-axis", df.columns, key="uniquekey_x_3D_line"
            )
            y_col = st.selectbox(
                "Select a column for the Y-axis", df.columns, key="uniquekey_y_3D_line"
            )
            z_col = st.selectbox(
                "Select a column for the Z-axis", df.columns, key="uniquekey_z_3D_line"
            )
            st.pyplot(create_3d_line_plot(df, x_col, y_col, z_col))

    # corellation Matrices
    correlation_matrix1 = df.select_dtypes(include=['number']).corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix1, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Pearson Correlation Matrix Heatmap")
    st.pyplot(plt)