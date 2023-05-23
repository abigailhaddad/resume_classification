import pandas as pd
import openai
import time
import json
from requests.exceptions import ReadTimeout


def load_api_key(path):
    with open(path, "r") as key_file:
        return key_file.read().strip()



def compose_prompt(row):
    """Compose prompt using fields from a DataFrame row."""
    overall_prompt="Please compose a sample resume using real years and institutions for the following person. Please go into a lot of detail and make this longer than you would think to, particularly the descriptions of what they're doing at their jobs."
    prompt = f"{overall_prompt} + {row['Name']} currently has the job title of {row['Current Job']}. They have an undergraduate degree in {row['Academic Background']}. This is a description of them: {row['Descriptions']}."
    print(prompt)
    return prompt


def get_response(prompt, engine):
    """Interact with OpenAI API and get a response to a given prompt."""
    messages = [{"role": "user", "content": prompt}]

    MAX_RETRIES = 5
    attempts = 0

    while attempts < MAX_RETRIES:
        try:
            response = openai.ChatCompletion.create(
                model=engine,
                messages=messages,
                max_tokens=1024,  
                temperature=0.0
            )
            return response.choices[0]['message']['content']

        # Handle too many tokens error
        except openai.error.InvalidRequestError as e:
            try:
                error_dict = json.loads(e.args[0])
                if 'too many tokens' in error_dict['message']:
                    tokens_allowed = int(error_dict['message'].split(' ')[-1])
                    tokens_in_prompt = len(openai.encode(prompt))

                    # Shorten the text by the excess tokens + some buffer
                    tokens_to_remove = tokens_in_prompt - tokens_allowed + 5
                    prompt = prompt[:-tokens_to_remove]

                else:
                    print(f"Unexpected InvalidRequestError: {str(e)[:100]}")
                    return ''

            except json.JSONDecodeError:
                print(f"Failed to parse error message: {e.args[0]}")
                return ''

        # Handle model overloaded error
        except openai.error.RateLimitError as e:
            if attempts < MAX_RETRIES:
                attempts += 1
                print(f"Model overloaded, retrying... (Attempt {attempts})")
                time.sleep(10)  # Wait before retrying
            else:
                print(f"Error processing prompt. Engine: {engine}, Prompt: {prompt}, Error: {str(e)[:100]}")
                return ''
            
        # Handle timeout error
        except ReadTimeout as e:
            if attempts < MAX_RETRIES:
                attempts += 1
                print(f"Request timed out, retrying... (Attempt {attempts})")
                time.sleep(10)  # Wait before retrying
            else:
                print(f"Error processing prompt due to timeout. Engine: {engine}, Prompt: {prompt}, Error: {str(e)[:100]}")
                return ''


        # Handle other exceptions
        except Exception as e:
            print(f"Error processing prompt. Engine: {engine}, Prompt: {prompt}, Error: {str(e)[:100]}")
            return ''


def process_responses(df, engine):
    """Get responses from GPT model for each row in the DataFrame."""
    df[f"response_{engine}"] = df.apply(lambda row: get_response(compose_prompt(row), engine), axis=1)
    return df



def main(input_file, output_file, n=None):
    # Load API key
    openai.api_key = load_api_key("../../key/key.txt")
    # Load and process data
    df = pd.read_excel(f"../data/{input_file}.xlsx")
    df = process_responses(df, 'gpt-4')
    #df.to_csv(f"../data/{output_file}.csv")
    return(df)


