import os
os.environ['OPENAI_API_KEY'] = ''

import json
import copy
from tqdm import tqdm
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_injection_prompt_meta(prompt_filename: str, meta_filename: str):
    prompt = str()
    with open(prompt_filename) as f:
        prompt = f.read()
    with open(meta_filename) as f:
        meta = json.load(f)
    return prompt, meta

def chat_completion(content: str):
    res = client.chat.completions.create(
        messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
        model="gpt-4o",
    )
    return res.choices[0].message.content

def get_content(prompt: str, entry: dict):
    content = copy.deepcopy(prompt)
    filename = 'inject_{@program_name}.py'
    filename = filename.replace('{@program_name}', entry['fault_name'])
    content = content.replace('{@file_name}', filename)
    content = content.replace('{@program_description}', entry['detailed_description'])
    return (filename, content)

def dump_to_dir(dirname: str, filename: str, text: str):
    with open(f'{dirname}/{filename}', 'w') as f:
        f.write(text)

if __name__ == '__main__':
    prompt, meta = get_injection_prompt_meta('Injection_generation_prompt.txt', 'Injection_meta.json')
    for m in tqdm(meta): 
        filename, content = get_content(prompt, m)
        # print(content)
        llm_response = chat_completion(content)
        dump_to_dir('more_injectors', filename, llm_response)