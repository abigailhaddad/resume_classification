# Project Title: Resume Evaluator

## Description

This project contains Python code for evaluating resumes for data science roles. It leverages AI models to generate and evaluate synthetic resumes.

The project contains three main components:

1. `generate_resumes.py`: This module is used for generating synthetic resumes using an AI model.

2. `gpt_prompt_software.py`: This module is used for evaluating the synthetic resumes using another AI model.

3. `model_evaluation_formal.py`: This module is used to analyze the responses from the AI model and calculate cross-tabulations.

4. `main.py`: This script orchestrates the entire process by calling the functions in the above modules in the correct order.

## Requirements

The project requires the following Python libraries:

- `pandas`
- `openai`
- `tabulate`
- `json`
- `unicodedata`
- `time`
- `requests`

## Usage

First, ensure that all required libraries are installed in your Python environment. Then, navigate to the project directory and run the `main.py` script:

```bash
python main.py
```

### File Descriptions

- `main.py`: Main script that orchestrates the entire process.
- `generate_resumes.py`: Module for generating synthetic resumes.
- `gpt_prompt_software.py`: Module for evaluating synthetic resumes.
- `model_evaluation_formal.py`: Module for analyzing AI model responses and calculating cross-tabulations.
- `key.txt`: Your OpenAI API key (not provided in the repository, you have to provide it).

### Inputs

The main input is a series of prompts defined in `main.py`, which are used for evaluating the synthetic resumes.

### Outputs

The output is a .csv file containing synthetic resumes and their evaluations, as well as a .txt file containing cross-tabulation tables.

## Note

This project uses OpenAI's GPT-4 and GPT-3.5-turbo models. Please ensure you have API access to these models and have the necessary keys and tokens.