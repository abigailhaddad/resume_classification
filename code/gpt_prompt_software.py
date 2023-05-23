import pandas as pd
import openai
import time
import json
import unicodedata

def strip_control_characters(input_string):
    # This will replace all control characters with a space
    return ''.join(char if unicodedata.category(char)[0]!="C" else ' ' for char in input_string)



def load_api_key(path):
    with open(path, "r") as key_file:
        return key_file.read().strip()


def load_data(path):
    """Load data from a csv file."""
    return pd.read_csv(path)

def get_response(prompt, engine):
    """Interact with OpenAI API and get a response to a given prompt."""
    cleaned_prompt = strip_control_characters(prompt)
    
    MAX_RETRIES = 5
    attempts = 0
    
    while attempts < MAX_RETRIES:
        messages = [{"role": "user", "content": cleaned_prompt}]  # Move this line here

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
                    tokens_in_prompt = len(openai.encode(cleaned_prompt))

                    # Shorten the text by the excess tokens + some buffer
                    tokens_to_remove = tokens_in_prompt - tokens_allowed + 5
                    cleaned_prompt = cleaned_prompt[:-tokens_to_remove]

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
                print(f"Error processing prompt. Engine: {engine}, Prompt: {cleaned_prompt}, Error: {str(e)[:100]}")
                return ''
            
        # Handle OpenAI error, including Bad Gateway error
        except openai.error.OpenAIError as e:
            attempts += 1
            print(f"OpenAI error, retrying... (Attempt {attempts})")
            if attempts == MAX_RETRIES:
                print(f"Failed after {MAX_RETRIES} attempts. Error: {str(e)[:100]}")
                return ''
            time.sleep(10)  # Wait before retrying
    
        
        # Handle other exceptions
        except Exception as e:
            print(f"Error processing prompt. Engine: {engine}, Prompt: {cleaned_prompt}, Error: {str(e)[:100]}")
            return ''

def process_responses(df, engine, prompt_dict):
    """Get responses from GPT model for each row in the DataFrame."""
    for prompt_key, prompt_value in prompt_dict.items():
        df[f"{prompt_key}_{engine}"] = df.apply(
            lambda row: get_response(f"{prompt_value}:: {row['response_gpt-4']}", engine), axis=1)
    return df


def main(input_file, output_file, prompt_dict, n=None):
    # Load API key
    openai.api_key = load_api_key("../../key/key.txt")
    # Load and process data
    df = load_data(f"../data/{input_file}.csv")
    if n:
        passed_resumes = df[df['Label'] == 1].sample(n)
        failed_resumes = df[df['Label'] == 0].sample(n)
        # Concatenate the sampled resumes
        df = pd.concat([passed_resumes, failed_resumes])
    df = process_responses(df, 'gpt-3.5-turbo', prompt_dict)
    df.to_csv(f"../data/{output_file}.csv")
    return(df)


