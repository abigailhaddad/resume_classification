import os
import pandas as pd
from PyPDF2 import PdfReader
import textract
import re

def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = " ".join([page.extract_text() for page in pdf.pages])
    return text

def process_files():
    # Specify directory where your resumes are stored
    directory = os.path.join("..", "data")

    # Initialize empty DataFrame
    df = pd.DataFrame(columns=['filename', 'text'])

    # Read and process files
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf") or file.endswith(".docx"):
                filepath = subdir + os.sep + file

                if file.endswith(".pdf"):
                    text = extract_text_from_pdf(filepath)
                elif file.endswith(".docx"):
                    text = textract.process(filepath).decode('utf-8')
                
                # Lowercase filename, remove extension and non-alphabetical characters
                file = file.lower()
                file = ".".join(file.split('.')[:-1]) # Remove the extension
                file = re.sub(r'[^a-z]', '', file) # Remove non-alphabetical characters
                
                df = df.append({'filename': file, 'text': text}, ignore_index=True)
    return df

def main(output_file):
    df = process_files()
    labels = pd.read_excel(r"..\data\fake_resume_labels.xlsx")
    
    # Lowercase 'Resume Name' field, remove extension and non-alphabetical characters
    labels['Resume Name'] = labels['Resume Name'].str.lower()
    labels['Resume Name'] = labels['Resume Name'].str.split('.').str[:-1].str.join('.') # Remove the extension
    labels['Resume Name'] = labels['Resume Name'].str.replace(r'[^a-z]', '') # Remove non-alphabetical characters

    # Merge df and labels dataframes
    merged_df = pd.merge(df, labels, left_on='filename', right_on='Resume Name', how='inner')
    merged_df.to_csv(f"../data/{output_file}.csv")
    return(merged_df)
