# import necessary libraries
import streamlit as st
import pandas as pd
import datetime

# function to clean the date format
def clean_date_format(date_column):
    cleaned_dates = []
    for date in date_column:
        try:
            cleaned_date = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%Y/%m/%d')
        except:
            try:
                cleaned_date = datetime.datetime.strptime(str(date), '%d/%m/%Y').strftime('%Y/%m/%d')
            except:
                try:
                    cleaned_date = datetime.datetime.strptime(str(date), '%m/%d/%Y').strftime('%Y/%m/%d')
                except:
                    cleaned_date = "Invalid Date"
        cleaned_dates.append(cleaned_date)
    return cleaned_dates

def main():
    st.title("DOB Format Cleaner")
    
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])
    
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        st.write(df)
        
        col_name = st.text_input("Enter the column name with Date of Birth")
        
        if col_name:
            if col_name not in df.columns:
                st.error("This column does not exist in the dataframe.")
            else:
                df[f"{col_name}_cleaned"] = clean_date_format(df[col_name])
                st.write(df)
                
                # Download Link
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_file.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
