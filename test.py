import random

from textblob import TextBlob

# Predefined dictionaries for names, verbs, and places for each letter
names_dict = {
    'a': ['Amit', 'Asha', 'Anil', 'Aarti', 'Arjun', 'Ananya', 'Ankit'],
    'b': ['Bala', 'Bhavna', 'Bobby', 'Bina', 'Bharat', 'Bharathi', 'Binod'],
    'c': ['Chitra', 'Chirag', 'Chetan', 'Chandni', 'Charan', 'Chanchal', 'Chaya'],
    'd': ['Deepak', 'Disha', 'Dhruv', 'Divya', 'Dev', 'Dipti', 'Dinesh'],
    'e': ['Esha', 'Eshan', 'Ekta', 'Eklavya', 'Eesha', 'Eshita', 'Ekansh'],
    'f': ['Firoz', 'Farah', 'Fahim', 'Falguni', 'Fateh', 'Farida', 'Faiyaz'],
    'g': ['Geeta', 'Gaurav', 'Gulab', 'Gita', 'Gagan', 'Gayatri', 'Govind'],
    'h': ['Hari', 'Hina', 'Harish', 'Hema', 'Hiren', 'Harsha', 'Heena'],
    'i': ['Isha', 'Ishan', 'Indra', 'Indu', 'Ira', 'Ishwar', 'Ishita'],
    'j': ['Jatin', 'Jaya', 'Jyoti', 'Javed', 'Jitendra', 'Jagruti', 'Jignesh'],
    'k': ['Karan', 'Kiran', 'Kavita', 'Kishore', 'Kriti', 'Kamala', 'Kunal'],
    'l': ['Lata', 'Lalit', 'Leela', 'Lokesh', 'Lakshmi', 'Luv', 'Lavanya'],
    'm': ['Mohan', 'Mira', 'Manish', 'Meera', 'Mahesh', 'Madhuri', 'Mukesh'],
    'n': ['Nitin', 'Nina', 'Nikhil', 'Neha', 'Naveen', 'Nalini', 'Nandini'],
    'o': ['Om', 'Ojas', 'Omkar', 'Oviya', 'Ojasvi', 'Omisha', 'Onkar'],
    'p': ['Pooja', 'Pranav', 'Priya', 'Pavan', 'Priti', 'Puneet', 'Pallavi'],
    'q': ['Qasim', 'Qamar', 'Quadir', 'Qadira', 'Qazi', 'Quila', 'Qamar'],
    'r': ['Ravi', 'Rina', 'Rohit', 'Rekha', 'Raj', 'Rashmi', 'Ramesh'],
    's': ['Sunil', 'Sneha', 'Suresh', 'Sonia', 'Sanjay', 'Sapna', 'Sumit'],
    't': ['Tina', 'Tarun', 'Trisha', 'Tejas', 'Tanvi', 'Tushar', 'Tulsi'],
    'u': ['Usha', 'Uday', 'Uma', 'Umesh', 'Urvashi', 'Upen', 'Utkarsh'],
    'v': ['Vijay', 'Veena', 'Vinod', 'Vani', 'Varun', 'Vidya', 'Vikram'],
    'w': ['Wasim', 'Wahid', 'Wajid', 'Wafiya', 'Waheeda', 'Waman', 'Wahida'],
    'x': ['Xavier', 'Xara', 'Xena', 'Xavian', 'Xia', 'Xavi', 'Xina'],
    'y': ['Yash', 'Yasmin', 'Yogesh', 'Yamini', 'Yuvraj', 'Yashoda', 'Yatin'],
    'z': ['Zara', 'Zain', 'Zoya', 'Zubair', 'Zaina', 'Zafar', 'Zulekha']
}

verbs_dict = {
    'a': ['ask', 'arrange', 'assemble', 'achieve', 'advise'],
    'b': ['build', 'bring', 'buy', 'bake', 'borrow'],
    'c': ['create', 'collect', 'carry', 'clean', 'cook'],
    'd': ['dance', 'draw', 'design', 'develop', 'discover'],
    'e': ['explore', 'eat', 'enjoy', 'examine', 'enter'],
    'f': ['find', 'fix', 'fold', 'follow', 'fetch'],
    'g': ['grow', 'give', 'gather', 'guide', 'gain'],
    'h': ['help', 'hold', 'hunt', 'heal', 'hug'],
    'i': ['imagine', 'invite', 'improve', 'inspect', 'inspire'],
    'j': ['join', 'jump', 'jog', 'juggle', 'judge'],
    'k': ['kick', 'keep', 'knit', 'know', 'knead'],
    'l': ['learn', 'lift', 'lead', 'look', 'listen'],
    'm': ['make', 'move', 'mix', 'measure', 'meet'],
    'n': ['notice', 'nurture', 'name', 'negotiate', 'navigate'],
    'o': ['observe', 'organize', 'open', 'offer', 'obtain'],
    'p': ['play', 'plan', 'prepare', 'plant', 'paint'],
    'q': ['question', 'quench', 'queue', 'quote', 'quiet'],
    'r': ['read', 'run', 'raise', 'ride', 'repair'],
    's': ['sing', 'swim', 'study', 'sell', 'see'],
    't': ['talk', 'teach', 'travel', 'tell', 'taste'],
    'u': ['use', 'understand', 'unlock', 'unite', 'update'],
    'v': ['visit', 'view', 'value', 'volunteer', 'venture'],
    'w': ['walk', 'write', 'watch', 'wash', 'wish'],
    'x': ['xerox', 'x-ray', 'x-out', 'x-amine', 'x-pand'],
    'y': ['yawn', 'yell', 'yield', 'yodel', 'yoke'],
    'z': ['zoom', 'zigzag', 'zap', 'zone', 'zip']
}

places_dict = {
    'a': ['Agra', 'Ahmedabad', 'Amritsar', 'Allahabad', 'Aurangabad'],
    'b': ['Bangalore', 'Bhopal', 'Bhubaneswar', 'Baroda', 'Bombay'],
    'c': ['Chennai', 'Coimbatore', 'Chandigarh', 'Cuttack', 'Calicut'],
    'd': ['Delhi', 'Dehradun', 'Dhanbad', 'Darjeeling', 'Durgapur'],
    'e': ['Ernakulam', 'Erode', 'Eluru', 'Ettumanoor', 'Etawah'],
    'f': ['Faridabad', 'Firozabad', 'Fatehpur', 'Fazilka', 'Faizabad'],
    'g': ['Gurgaon', 'Gwalior', 'Gandhinagar', 'Guntur', 'Ghaziabad'],
    'h': ['Hyderabad', 'Hubli', 'Haldia', 'Hoshiarpur', 'Hapur'],
    'i': ['Indore', 'Imphal', 'Itanagar', 'Idukki', 'Ichalkaranji'],
    'j': ['Jaipur', 'Jodhpur', 'Jalandhar', 'Jamshedpur', 'Jabalpur'],
    'k': ['Kolkata', 'Kanpur', 'Kota', 'Kochi', 'Kurnool'],
    'l': ['Lucknow', 'Ludhiana', 'Latur', 'Lonavala', 'Leh'],
    'm': ['Mumbai', 'Madurai', 'Mysore', 'Meerut', 'Moradabad'],
    'n': ['Nagpur', 'Nashik', 'Noida', 'Nainital', 'Nanded'],
    'o': ['Ooty', 'Osmanabad', 'Ongole', 'Ottapalam', 'Orchha'],
    'p': ['Pune', 'Patna', 'Pondicherry', 'Panipat', 'Porbandar'],
    'q': ['Quilon', 'Quazigund', 'Quepem', 'Quilon', 'Quirihalla'],
    'r': ['Ranchi', 'Ratnagiri', 'Rourkela', 'Rajahmundry', 'Rewa'],
    's': ['Surat', 'Shimla', 'Srinagar', 'Satara', 'Solapur'],
    't': ['Trivandrum', 'Tirupati', 'Thane', 'Tiruchirappalli', 'Thanjavur'],
    'u': ['Udaipur', 'Ujjain', 'Una', 'Unjha', 'Udupi'],
    'v': ['Varanasi', 'Vadodara', 'Vellore', 'Vijayawada', 'Visakhapatnam'],
    'w': ['Warangal', 'Wardha', 'Wayanad', 'Wankaner', 'Washim'],
    'x': ['Xiangyang', 'Xianning', 'Xiaoshan', 'Xingtai', 'Xinyu'],
    'y': ['Yanam', 'Yinchuan', 'Yongzhou', 'Yichang', 'Yulin'],
    'z': ['Zunyi', 'Zigong', 'Zhuhai', 'Zhaotong', 'Ziyang']
}






def generate_story(input_str, templates):
    input_letters = list(input_str)
    story_templates = templates[:]
    story = []

    # Choose a random template from the list
    template = random.choice(story_templates)
    
    replaced_template = []
    words = template.split()
    
    for word in words:
        if word == '{NN}':
            letter = input_letters.pop(0).lower()
            word = random.choice(names_dict.get(letter, ['Unknown']))
        elif word == '{VB}':
            letter = input_letters.pop(0).lower()
            word = random.choice(verbs_dict.get(letter, ['Unknown']))
        elif word == '{place}':
            letter = input_letters.pop(0).lower()
            word = random.choice(places_dict.get(letter, ['Unknown']))
        
        replaced_template.append(word)
    
    story.append(' '.join(replaced_template))
    
    return story


# Example usage:
templates_4=[
    "Long ago in {place} , {NN} and {NN} found a mystical {VB} that changed their lives forever.",
    "In a small village called {place} , {NN} was known for {VB} and {NN} loved to join in.",
    "Long ago in {place} , {NN} discovered a hidden treasure while {VB} with {NN} ."
]
templates_5 = [
    "In the enchanting city of {place} , {NN} , {NN} , and {NN} embarked on a journey to {VB} and discovered hidden treasures.",
    "Once upon a time, in the town of {place} , {NN} and {NN} met {NN} who taught them how to {VB} with passion.",
    "At {place} , {NN} , {NN} , and {NN} would {VB} under the stars, dreaming of adventures yet to come.",
    "In a small village called {place} , {NN} , {NN} , and {NN} were known for their {VB} skills.",
   
    
]

templates_6 = [
    "In the heart of {place} , {NN} , {NN} , and {NN} embarked on a journey to {VB} and discover the secrets of life. They found {place} to be a place of mystery.",
    "At {place} , {NN} , {NN} , and {NN} gathered every evening to {VB} and reflect on their day. The atmosphere of {place} always filled them with a sense of calm and inspiration."
    "Long ago in {place} , {NN} , {NN} , {NN} , and {NN} discovered a hidden treasure while they were {VB} ."
]

templates_7 = [
   "In the bustling city of {place} , {NN} , {NN} ,and {NN} were known for their ability to {VB} and explore new {place} . They would often {VB} together under the vibrant city lights."
   "Once upon a time, in the town of {place} , there lived {NN} , {NN} , {NN} , {NN} , and {NN}. They loved to {VB} every day.",
]

templates_8 = [
   
    "{NN} , {NN} , {NN} , {NN} , and {NN} met at {place} where they {VB} and found a deep connection that transcended time and space. They would often {VB} together, sharing stories and dreams with each other."


]

templates_9 = [

    "In the city of {place} , {NN} , and {NN} met {NN} , {NN} , and {NN} who taught them how to {VB} with passion. Together, they explored {place} and discovered a hidden {VB} that changed their lives forever."

]

def extract_first_letters(text):
    # Split the text into words
    words = text.split()

    # Extract the first letter of each of the first `num_words` words and convert to lowercase
    first_letters = [word[0].lower() for word in words]

    # Join the first letters into a single string
    result = ''.join(first_letters)

    return result
def append_keywords_to_story(output, story):
    # Formatting the output string
    formatted_output = f"<b>Extracted Initial Letters = {'  '.join(output)}</b> </br></br>"
    # Appending the formatted output to the story
    story = f"{formatted_output}{story}"
    return story


def story(input_string):
    # Choose templates based on the length of input_string
    output = extract_first_letters(input_string)
    if len(output) == 4:
        templates = templates_4
    elif len(output) == 5:
        templates = templates_5    
    elif len(output) == 6:
        templates = templates_6
    elif len(output) == 7:
        templates = templates_7
    elif len(output) == 8:
        templates = templates_8
    elif len(output) >= 9:
        templates = templates_9
    # Generate and print the story
    story = generate_story(output, templates)

    final_story = append_keywords_to_story(output, story)

    return final_story


