from flask import Flask, request, jsonify
from flask_cors import CORS
import random
# from KeyLetterFinal import start
from test import story
from lemma import process_words
from keytotext import pipeline


app = Flask(__name__)
CORS(app)  # Enable CORS

def split_string_to_list(input_text):
    return input_text.split()


def k2t_base(input_text):
    nlp = pipeline("k2t-base")
    # list = split_string_to_list(input_text)
    list = process_words(input_text)
    return nlp(list)

def k2t(input_text):
    nlp = pipeline("k2t")
    list = process_words(input_text)
    return nlp(list)


def eachword(input_text):
    from keytotext import pipeline
    nlp = pipeline("mrm8488/t5-base-finetuned-common_gen")
    list = process_words(input_text)
    return nlp(list)


def generate_sentence(input_text,model):
    if(model=="lite"):
        res = story(input_text)
        return res
    elif(model == 'base'):
        res = k2t_base(input_text)
        return res
    else:
        res = eachword(input_text)
        return res


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    input_text = data.get('input_text', '')
    model = data.get('model', '')  # Get the model value from the request
    print(input_text)
    generated_sentence = generate_sentence(input_text,model)
    return jsonify({'generated_sentence': generated_sentence})

if __name__ == '__main__':
    app.run(debug=True)



    

# def select_letters(text, num_letters):
#     # Split the text into words
#     words = text.split()
    
#     selected_letters = []
#     for word in words:
#         # Select the first num_letters characters of each word
#         selected_letters.append(word[:num_letters])
    
#     return selected_letters

# # Example usage
# text = "This is an example sentence for selecting letters"
# selected_2_letters = select_letters(text, 2)
# selected_3_letters = select_letters(text, 3)

# print("First 2 letters of each word:", selected_2_letters)
# print("First 3 letters of each word:", selected_3_letters)


# # Function to read words from a text file
# def read_words_from_file():
#     with open('words.txt', 'r') as file:
#         words = file.read().splitlines()
#     return words

# # Function to generate a sentence from given letters
# def generate_sentence(letters, word_list):
#     sentence = []
    
#     for letter in letters:
#         # Find words starting with the given letter
#         candidates = [word for word in word_list if word.lower().startswith(letter.lower())]
#         if candidates:
#             # Choose a random word
#             chosen_word = random.choice(candidates)
#             sentence.append(chosen_word)
#         else:
#             sentence.append(f" ")
    
#     return ' '.join(sentence)

# # Read words from the text file
# word_list = read_words_from_file()
# selected_3_letters = select_letters(text, 3) #selected_3_letters = ['pl', 'def', 'de', 'dev', 'te']







