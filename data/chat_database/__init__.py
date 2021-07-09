from pathlib import Path
import json
import pandas as pd

def load_intents(location):
    intents_data = Path(location).read_text()
    return json.loads(intents_data)['intents']
data_collection = load_intents("Intent.json")

def level_list(list_input, target_size):
    result = []
    while True:
        if len(result) >= target_size:
            break
        else:
            result += list_input
    return result[:target_size]

dataset = pd.DataFrame(columns=['intent', 'text', 'response'])

for data in data_collection:
    intent = data['intent']
    texts = level_list(data['text'], len(data['responses']))
    for text, response in zip(texts, data['responses']):
        row = {'intent': intent, 'text': text, 'response': response}
        dataset = dataset.append(row, ignore_index=True)