# Import necessary libraries
import streamlit as st
import pandas as pd
import base64
import chardet

# Detect encoding of the file
def detect_encoding(file_buffer):
    result = chardet.detect(file_buffer.read())
    file_buffer.seek(0)
    return result['encoding']

# Function to clean the date format
def clean_date_format(date_column):
    cleaned_dates = []
    for date in date_column:
        try:
            # Use pandas to automatically detect the date format
            dt = pd.to_datetime(str(date))
            cleaned_date = dt.strftime('%Y/%m/%d')
        except:
            cleaned_date = "Invalid Date"
        cleaned_dates.append(cleaned_date)
    return cleaned_dates

def main():
    st.title("DOB Format Cleaner")
    
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])
    
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            encoding = detect_encoding(uploaded_file)
            df = pd.read_csv(uploaded_file, encoding=encoding,delimiter=';')
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        st.write(df)

        # Use a selectbox for column selection
        col_name = st.selectbox("Select the column with Date of Birth", df.columns)

        if col_name:
            df[f"{col_name}_cleaned"] = clean_date_format(df[col_name])
            st.write(df[[col_name,f"{col_name}_cleaned"]])
                
            # Provide a download link for the cleaned CSV
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Convert bytes to string
            href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_file.csv">Download Cleaned CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
