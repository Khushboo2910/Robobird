import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


qa_pairs = {
    "what is your name": "I am a chatbot.",
    "how are you": "I am just a bunch of code",
    "what can you do": "I can chat with you and answer simple questions.",
    "goodbye": "Goodbye! Have a great day!"
}

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(user_input):
    tokens = word_tokenize(user_input)
    tokens = [word.lower() for word in tokens]
    tokens = [word for word in tokens if word.isalnum()]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def chatbot():
    print("Chatbot: Hello! How can I help you?")
    
    while True:
        user_input = input("You: ")
        print(f"Debug: User input: {user_input}")  
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! Have a nice day!")
            break
        
        preprocessed_input = preprocess(user_input)
        print(f"Debug: Preprocessed input: {preprocessed_input}")  
        
        response = qa_pairs.get(preprocessed_input, "I'm sorry, I don't understand that question.")
        
        print(f"Chatbot: {response}")

if __name__ == '__main__':
    chatbot()
