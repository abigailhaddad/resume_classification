import pandas as pd
from tabulate import tabulate

def clean_response(text):
    """Clean the response received from GPT model."""
    text=str(text)
    if "YES" in text:
        return "Y"
    elif "NO" in text:
        return "N"
    else:
        return text
    

def clean_data(df, engine, prompt_dict):
    """Clean the data in the DataFrame."""
    for prompt_key in prompt_dict.keys():
        if prompt_key!="summary":
            df[f"{prompt_key}_{engine}_answer"] = df[f"{prompt_key}_{engine}"].apply(clean_response)
    return df

def calculate_crosstabs(df):
    """Calculate and return the crosstabs for each answer column."""
    answer_cols = [col for col in df.columns if col.endswith("_answer")]
    crosstab_tables = {}
    
    for col in answer_cols:
        crosstab_table = pd.crosstab(df["Label"], df[col])
        crosstab_tables[col] = crosstab_table
        
    return crosstab_tables

def write_crosstab_tables(crosstab_tables, output_file):
    """Write the crosstab tables to the output file."""
    with open(output_file, "w") as file:
        for col, table in crosstab_tables.items():
            file.write(f"Prompt: {col}\n\n")
            file.write(tabulate(table, headers="keys", tablefmt="grid"))
            file.write("\n\n")

def main(input_file, output_file, prompt_dict):
    # Assuming you have a DataFrame `df` with your data and model predictions
    df = pd.read_csv(f"../data/{input_file}.csv")
    
    # Clean the data for the specified engine
    engine = "gpt-3.5-turbo"
    df = clean_data(df, engine, prompt_dict)

    # Calculate crosstabs
    crosstab_tables = calculate_crosstabs(df)

    # Write crosstab tables to the output file
    write_crosstab_tables(crosstab_tables, f'{output_file}.txt')


