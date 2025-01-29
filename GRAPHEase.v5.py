import streamlit as st
import plotly.express as px
import pandas as pd
import os
from datetime import datetime
import pdfkit
import tempfile

# Ensure this path points to the folder containing wkhtmltopdf.exe
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Function to generate PDF
def generate_pdf(chart_html, chart_title, report_date, report_time, prepared_by):
    # Create HTML content for the PDF
    pdf_content = f"<h1>{chart_title}</h1><p>Date: {report_date}<br>Time: {report_time}<br>Prepared by: {prepared_by}</p>"
    full_html = f"<div>{pdf_content}<br>{chart_html}</div>"

    # Create a temporary file to save PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file_path = tmp_file.name
        # Generate PDF from the HTML content
        pdfkit.from_string(full_html, tmp_file_path, configuration=config)
        return tmp_file_path

# Function to load CSS for the app
def load_css(css_file):
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"CSS file {css_file} not found. Please check the file path.")

# Function to display Home page
def home_page():
    st.title('Welcome to GRAPHEase')
    st.write("""
        **Transform your data into impactful visual stories!**

        **GRAPHEase** is your go-to tool for creating interactive and customizable data visualizations, designed to make education, research, and innovation 
        more accessible and engaging. Whether you're a student, educator, or professional, **GRAPHEase** empowers you to represent knowledge visually and 
        communicate insights effectively.

        **Upload. Visualize. Innovate.**
        Get started today and unlock the potential of your data!
    """)

# Function to display About page
def about_page():
    st.title('About GRAPHEase')
    st.write("""
        Welcome to **GRAPHEase**, a powerful and user-friendly data visualization tool designed to empower education, innovation, and knowledge representation.
        
        At GRAPHEase, we believe that data is more than just numbers—it's a story waiting to be told. Our platform transforms raw datasets into insightful 
        visualizations, making it easy for educators, students, researchers, and professionals to understand and communicate complex information effectively.
        
        ## Why GRAPHEase?
        **Education Made Visual**: Data visualization helps simplify learning by representing complex concepts in charts, graphs, and interactive visuals. 
        Perfect for classrooms and self-study!
        
        **Empowering Innovation**: Innovators and researchers can explore trends, correlations, and patterns to fuel groundbreaking discoveries.
        
        **Intuitive & Accessible**: Upload your dataset, customize visual settings, and watch your data come to life—no coding experience needed.
        
        **Comprehensive Chart Options**: From scatter plots to pie charts, bar graphs to line charts, GRAPHEase provides a wide range of options to suit your needs.
        
        ## Our Mission
        GRAPHEase aims to democratize data visualization, bridging the gap between information and understanding. By providing a simple yet powerful platform, 
        we empower users to make informed decisions, share knowledge, and innovate with clarity.
        
        ## Who Is It For?
        - **Educators**: Create compelling visuals to engage students in the classroom.
        - **Students**: Represent project data and research in a clear, professional way.
        - **Researchers**: Identify trends and insights hidden in raw data.
        - **Professionals**: Simplify presentations and decision-making with impactful visuals.
        
        Join us in transforming the way knowledge is represented and shared. Together, we can bridge the gap between data and discovery, unlocking the 
        potential for education and innovation.
        
        **Start your visualization journey with GraphEase today!**
    """)

# Sidebar navigation
page = st.sidebar.radio("Select a page", ("Home", "About", "Visualizations"))

# Show pages based on user selection
if page == "Home":
    home_page()
elif page == "About":
    about_page()

# For visualizations, keep the original content but only show if the page is "Visualizations"
if page == "Visualizations":
    # Visualization page introduction
    st.title('Data Visualizations')
    st.write("""
        Welcome to the Visualizations page! Here, you can easily upload your CSV or Excel file and start exploring your data through interactive charts.

        Choose from a variety of visualization options to uncover insights, identify trends, and present your data in compelling ways. Whether you're looking to analyze 
        relationships, trends, distributions, or patterns, GraphEase makes it simple to bring your data to life.

        Ready to get started? Upload your file and select the chart type that best suits your needs. Customize your visualizations and watch as your data transforms into valuable insights!
    """)

    # Add a sidebar for file upload
    st.sidebar.subheader('Visualization Settings')

    uploaded_file = st.sidebar.file_uploader(label="Upload your CSV or Excel file.", type=['csv', 'xlsx'])

    # Date and time input
    report_date = st.sidebar.date_input("Report Date", value=datetime.today().date())
    report_time = st.sidebar.time_input("Report Time", value=datetime.now().time())

    # Add a sidebar input for "Prepared by"
    prepared_by = st.sidebar.text_input("Prepared by:", value="Your Name")

    # Initialize variables
    df = None
    numeric_columns = []
    all_columns = []

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            
            # Extract numeric and all columns
            numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
            all_columns = list(df.columns)  # Include all columns for visualization
            st.write(df)
        except Exception as e:
            st.write(f"Error loading file: {e}")
    else:
        st.write("*Please upload a file to start.*")

    # Add a select widget to the sidebar
    chart_select = st.sidebar.selectbox(
        label="Select the Chart Type",
        options=['Scatterplots', 'Bar Chart', 'Pie Chart', 'Lineplots', 'Histogram', 'Boxplot']
    )

    # Ensure numeric_columns and df are properly initialized before proceeding
    if df is not None and numeric_columns:
        # For each chart type, show the settings and the title input at the end
        if chart_select == 'Scatterplots':
            st.sidebar.subheader("Scatterplot Settings")
            try:
                x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
                y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
                color_column = st.sidebar.selectbox('Color by', options=all_columns, index=0)
                # Title input at the end
                chart_title = st.sidebar.text_input("Title of Chart", value="Scatterplot of Data")
                plot = px.scatter(
                    data_frame=df, 
                    x=x_values, 
                    y=y_values, 
                    color=color_column,
                    title=chart_title
                )
                plot.update_layout(
                    annotations=[
                        dict(
                            text=f"Date: {report_date}<br>Time: {report_time}",
                            x=1,  # Position at the far right of the graph
                            y=1.28,  # Move further above the graph
                            xref="paper",  # Relative to the graph size
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"  # Align the text to the right
                        ),
                        dict(
                            text=f"Prepared by: {prepared_by}",
                            x=1,  # Align to the far right
                            y=-0.25,  # Move further down below Date and Time
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"
                        )                        
                    ]

                )
                st.plotly_chart(plot)

                #DOWNLOADABLE FILE AS PDF
                pdf_file = generate_pdf(plot.to_html(), chart_title, report_date, report_time, prepared_by)

                st.download_button(
                    label="Download Chart as PDF",
                    data=pdf_file,
                    file_name=f"{chart_title}.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.write(f"Error: {e}")

        # Similarly, add the PDF download functionality for Bar Chart, Histogram, Boxplot, etc.
        # Follow the same structure as above for each chart type


        elif chart_select == 'Bar Chart':
            st.sidebar.subheader("Bar Chart Settings")
            try:
                x_values = st.sidebar.selectbox('X axis', options=all_columns)
                y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
                color_column = st.sidebar.selectbox('Color by', options=all_columns, index=0)
                # Title input at the end
                chart_title = st.sidebar.text_input("Title of Chart", value="Bar Chart of Data")
                plot = px.bar(
                    data_frame=df, 
                    x=x_values, 
                    y=y_values, 
                    color=color_column,
                    title=chart_title
                )
                plot.update_layout(
                    annotations=[
                        dict(
                            text=f"Date: {report_date}<br>Time: {report_time}",
                            x=1,  # Position at the far right of the graph
                            y=1.28,  # Move further above the graph
                            xref="paper",  # Relative to the graph size
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"  # Align the text to the right
                        ),
                        dict(
                            text=f"Prepared by: {prepared_by}",
                            x=1,  # Align to the far right
                            y=-0.25,  # Move further down below Date and Time
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"
                        )                        
                    ]
                )
                st.plotly_chart(plot)

                #DOWNLOADABLE FILE AS PDF
                pdf_file = generate_pdf(plot.to_html(), chart_title, report_date, report_time, prepared_by)

                st.download_button(
                    label="Download Chart as PDF",
                    data=pdf_file,
                    file_name=f"{chart_title}.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.write(f"Error: {e}")

        elif chart_select == 'Pie Chart':
            st.sidebar.subheader("Pie Chart Settings")
            try:
                pie_column = st.sidebar.selectbox('Values', options=numeric_columns)
                name_column = st.sidebar.selectbox('Names', options=all_columns)
                # Title input at the end
                chart_title = st.sidebar.text_input("Title of Chart", value="Pie Chart of Data")
                plot = px.pie(
                    data_frame=df, 
                    values=pie_column, 
                    names=name_column,
                    title=chart_title  # Use the title input from the sidebar
                )
                plot.update_layout(
                    annotations=[
                        dict(
                            text=f"Date: {report_date}<br>Time: {report_time}",
                            x=1,  # Position at the far right of the graph
                            y=1.28,  # Move further above the graph
                            xref="paper",  # Relative to the graph size
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"  # Align the text to the right
                        ),
                        dict(
                            text=f"Prepared by: {prepared_by}",
                            x=1,  # Align to the far right
                            y=-0.25,  # Move further down below Date and Time
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"
                        )                        
                    ]
                )
                st.plotly_chart(plot)

                #DOWNLOADABLE FILE AS PDF
                pdf_file = generate_pdf(plot.to_html(), chart_title, report_date, report_time, prepared_by)

                st.download_button(
                    label="Download Chart as PDF",
                    data=pdf_file,
                    file_name=f"{chart_title}.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.write(f"Error: {e}")


        elif chart_select == 'Histogram':
            st.sidebar.subheader("Histogram Settings")
            try:
                hist_column = st.sidebar.selectbox('Select Column', options=numeric_columns)
                bins = st.sidebar.slider('Number of Bins', min_value=5, max_value=50, value=10)
                # Title input at the end
                chart_title = st.sidebar.text_input("Title of Chart", value="Histogram of Data")
                plot = px.histogram(
                    data_frame=df, 
                    x=hist_column, 
                    nbins=bins,
                )
                plot.update_layout(
                    annotations=[
                        dict(
                            text=f"Date: {report_date}<br>Time: {report_time}",
                            x=1,  # Position at the far right of the graph
                            y=1.28,  # Move further above the graph
                            xref="paper",  # Relative to the graph size
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"  # Align the text to the right
                        ),
                        dict(
                            text=f"Prepared by: {prepared_by}",
                            x=1,  # Align to the far right
                            y=-0.25,  # Move further down below Date and Time
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"
                        )                        
                    ]
                )
                st.plotly_chart(plot)

                #DOWNLOADABLE FILE AS PDF
                pdf_file = generate_pdf(plot.to_html(), chart_title, report_date, report_time, prepared_by)

                st.download_button(
                    label="Download Chart as PDF",
                    data=pdf_file,
                    file_name=f"{chart_title}.pdf",
                    mime="application/pdf"
                )                

            except Exception as e:
                st.write(f"Error: {e}")

        elif chart_select == 'Boxplot':
            st.sidebar.subheader("Boxplot Settings")
            try:
                x_values = st.sidebar.selectbox('X axis', options=all_columns)
                y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
                color_column = st.sidebar.selectbox('Color by', options=all_columns, index=0)
                # Title input at the end
                chart_title = st.sidebar.text_input("Title of Chart", value="Boxplot of Data")
                plot = px.box(
                    data_frame=df, 
                    x=x_values, 
                    y=y_values, 
                    color=color_column,
                )
                plot.update_layout(
                    annotations=[
                        dict(
                            text=f"Date: {report_date}<br>Time: {report_time}",
                            x=1,  # Position at the far right of the graph
                            y=1.28,  # Move further above the graph
                            xref="paper",  # Relative to the graph size
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"  # Align the text to the right
                        ),
                        dict(
                            text=f"Prepared by: {prepared_by}",
                            x=1,  # Align to the far right
                            y=-0.25,  # Move further down below Date and Time
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="gray"),
                            align="right"
                        )                        
                    ]
                )
                st.plotly_chart(plot)

                #DOWNLOADABLE FILE AS PDF
                pdf_file = generate_pdf(plot.to_html(), chart_title, report_date, report_time, prepared_by)

                st.download_button(
                    label="Download Chart as PDF",
                    data=pdf_file,
                    file_name=f"{chart_title}.pdf",
                    mime="application/pdf"
                )                

            except Exception as e:
                st.write(f"Error: {e}")

# Load CSS for footer and styling
load_css('style.css')

# Footer for the app
st.markdown("""
    <footer>
        <p>&copy; 2025 GRAPHEase. All rights reserved.<br>
        campos.jr.bsinfotech@gmail.com</p>
    </footer>
""", unsafe_allow_html=True)