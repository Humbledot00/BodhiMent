# -*- coding: utf-8 -*-
"""keyword.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K0nFe7s96o5DYcMx-FfXVRssMe6aU2Wq
"""

!pip install transformers pandas torch scikit-learn

# train_keyword_extractor.py

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForTokenClassification, AdamW
from sklearn.model_selection import train_test_split

class KeywordDataset(Dataset):
    def __init__(self, texts, keywords, tokenizer, max_length):
        self.texts = texts
        self.keywords = keywords
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        keywords = self.keywords[idx].split(', ')

        encoding = self.tokenizer(text, padding='max_length', truncation=True, max_length=self.max_length, return_tensors='pt')
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()

        labels = torch.zeros_like(input_ids)
        for keyword in keywords:
            keyword_encoding = self.tokenizer(keyword, add_special_tokens=False)
            keyword_ids = keyword_encoding['input_ids']

            for i in range(len(input_ids) - len(keyword_ids) + 1):
                if torch.all(input_ids[i:i+len(keyword_ids)] == torch.tensor(keyword_ids)):
                    labels[i:i+len(keyword_ids)] = 1

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }

def train_model():
    # Load and preprocess the data
    df = pd.read_csv('data.csv')

    # Split the data into train and test sets
    train_texts, test_texts, train_keywords, test_keywords = train_test_split(df['sentence'], df['keywords'], test_size=0.2, random_state=42)

    # Initialize the tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=2)

    # Create datasets and dataloaders
    max_length = 128
    train_dataset = KeywordDataset(train_texts.tolist(), train_keywords.tolist(), tokenizer, max_length)
    train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)

    # Training loop
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    optimizer = AdamW(model.parameters(), lr=5e-5)
    num_epochs = 5

    for epoch in range(num_epochs):
        model.train()
        for batch in train_dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")

    # Save the model and tokenizer
    model.save_pretrained('keyword_extractor_model')
    tokenizer.save_pretrained('keyword_extractor_tokenizer')

    print("Model and tokenizer saved successfully.")

if __name__ == "__main__":
    train_model()

# test_keyword_extractor.py

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForTokenClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support

class KeywordDataset(Dataset):
    def __init__(self, texts, keywords, tokenizer, max_length):
        self.texts = texts
        self.keywords = keywords
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        keywords = self.keywords[idx].split(', ')

        encoding = self.tokenizer(text, padding='max_length', truncation=True, max_length=self.max_length, return_tensors='pt')
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()

        labels = torch.zeros_like(input_ids)
        for keyword in keywords:
            keyword_encoding = self.tokenizer(keyword, add_special_tokens=False)
            keyword_ids = keyword_encoding['input_ids']

            for i in range(len(input_ids) - len(keyword_ids) + 1):
                if torch.all(input_ids[i:i+len(keyword_ids)] == torch.tensor(keyword_ids)):
                    labels[i:i+len(keyword_ids)] = 1

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }

def test_model():
    # Load the data
    df = pd.read_csv('data.csv')

    # Split the data into train and test sets
    _, test_texts, _, test_keywords = train_test_split(df['sentence'], df['keywords'], test_size=0.2, random_state=42)

    # Load the trained model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('keyword_extractor_tokenizer')
    model = BertForTokenClassification.from_pretrained('keyword_extractor_model')

    # Create test dataset and dataloader
    max_length = 128
    test_dataset = KeywordDataset(test_texts.tolist(), test_keywords.tolist(), tokenizer, max_length)
    test_dataloader = DataLoader(test_dataset, batch_size=8)

    # Evaluation
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in test_dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=2)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # Calculate metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        [label for labels in all_labels for label in labels],
        [pred for preds in all_preds for pred in preds],
        average='binary'
    )

    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

    # Function to extract keywords from a sentence
    def extract_keywords(sentence):
        encoding = tokenizer(sentence, padding='max_length', truncation=True, max_length=max_length, return_tensors='pt')
        input_ids = encoding['input_ids'].to(device)
        attention_mask = encoding['attention_mask'].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=2)

        keywords = []
        current_keyword = []
        for token, pred in zip(tokenizer.convert_ids_to_tokens(input_ids[0]), preds[0]):
            if pred == 1:
                current_keyword.append(token)
            elif current_keyword:
                keywords.append(tokenizer.convert_tokens_to_string(current_keyword).strip())
                current_keyword = []

        if current_keyword:
            keywords.append(tokenizer.convert_tokens_to_string(current_keyword).strip())

        return ', '.join(keywords)

    # Test the model on a new sentence
    test_sentence = "The Marathas fought against the British in the Anglo-Maratha Wars."
    extracted_keywords = extract_keywords(test_sentence)
    print(f"Sentence: {test_sentence}")
    print(f"Extracted Keywords: {extracted_keywords}")

if __name__ == "__main__":
    test_model()