import sys
import os
import nltk
from nltk.tokenize import sent_tokenize
import ssl
from rake_nltk import Rake
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from langdetect import detect, detect_langs
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn, words
import random
from random import choice
from nltk.corpus import brown



ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')
nltk.download('words')
nltk.download('brown')

def read_from_file(file_path):
    """ Cerinta 1: citeste un text dintr un fisier """
    
    if not os.path.isfile(file_path):
            print("not a file")
            sys.exit(0)
    
    text_from_file = []
    
    try:
        with open(file_path,'r') as f:
            text = f.read()
            text_from_file = text.split() 
                
    except Exception as e:
        print(e)
        return None
        
    return text_from_file

def detect_language(text):
    """ Cerinta 2: identifica limba textului """
    
    try:
        language = detect(text)
        probabilities = detect_langs(text)
        return language, probabilities
        
    except Exception as e:
        print(e)
        return None
    
def make_string_from_list(my_list):
    return " ".join(my_list)

def stylometric_analysis(text):
    """ Cerinta 3: Afiseaza informatii stilometrice """
    
    words_used = []
    for word in text.split():
        words_used.append(word.lower().strip(".,!?;:()[]{}\"'"))
        
    word_count = len(words_used)
    char_count = len(text)
    
    word_freq = Counter(words_used)
    
    unique_words = len(word_freq)
    
    lexical_density = unique_words / word_count if word_count > 0 else 0
    
    return {
        "word_count": word_count,
        "char_count": char_count,
        "word_frequency": word_freq,
        "unique_words": unique_words,
        "lexical_density": lexical_density
    }

def plot_word_frequencies(word_frequency):
    """ Pentru cerinta 3, reprezentare grafica (sa fie mai usor de vizualizat) """
    
    top_words = word_frequency.most_common(10)
    words, frequencies = zip(*top_words)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color='skyblue')
    plt.title("Top 10 Most Frequent Words", fontsize=16)
    plt.xlabel("Words", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.tight_layout()
    plt.show()
    
brown_words = Counter([word.lower() for word in brown.words()])   
common_words = set(words.words())

def filter_common_words(candidates):
    """Filtreaza cuvinte comune"""
    
    return [word for word in candidates if word in common_words and len(word) > 2 and word.isalpha()]

def prioritize_words(candidates):
    """Prioritizeaza cuvintele bazandu-se pe frecventa lor in corpusul Brown"""
    
    return sorted(candidates, key=lambda w: brown_words[w], reverse=True)

def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    filtered_synonyms = filter_common_words(list(synonyms))
    return prioritize_words(filtered_synonyms)

def get_hypernyms(word):
    hypernyms = set()
    for syn in wn.synsets(word):
        for hypernym in syn.hypernyms():
            hypernyms.update(lemma.name() for lemma in hypernym.lemmas())
    filtered_hypernyms = filter_common_words(list(hypernyms))
    return prioritize_words(filtered_hypernyms)

def get_antonyms(word):
    antonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.add(lemma.antonyms()[0].name())
    filtered_antonyms = filter_common_words(list(antonyms))
    return prioritize_words(filtered_antonyms)

pronouns_and_others = {
    "i", "me", "my", "mine", "myself",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "it", "its", "itself",
    "we", "us", "our", "ours", "ourselves",
    "they", "them", "their", "theirs", "themselves",
    "this", "that", "these", "those", "who", "whom", "whose", "which", "what",
    "everyone", "someone", "no one", "nobody", "anyone", "anybody", "each",
    "either", "neither", "none", "one", "a", "the","in","on","at","by","with"
}

def generate_alternatives(text):
    words = word_tokenize(text)
    new_text = []
    for word in words:
        lower_word = word.lower()
        if lower_word in pronouns_and_others:
            new_text.append(word)
        elif random.random() < 0.2:
            synonyms = get_synonyms(word)
            hypernyms = get_hypernyms(word)
            antonyms = get_antonyms(word)

            alternatives = synonyms + hypernyms
            if antonyms:
                alternatives.extend(["not " + antonym for antonym in antonyms])

            if alternatives:
                new_text.append(random.choice(alternatives))
            else:
                new_text.append(word)
        else:
            new_text.append(word)

    return " ".join(new_text)

def extract_keywords_with_rake(text, num_keywords=5):
    """Cerinta 5: extrage cuvintele cheie dintr un paragraf """
    
    rake = Rake()
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    return keywords[:num_keywords]

def generate_sentences_from_keywords(keywords, text):
    """Genereaza propozitii pentru fiecare cuv cheie"""
    
    sentences = sent_tokenize(text)
    keyword_sentences = {}

    creative_templates = [
        "The concept of '{keyword}' is fascinating and is highlighted in the sentence: {original_sentence}.",
        "A closer look at '{keyword}' reveals: {original_sentence}.",
        "An essential idea in this text is '{keyword}', as described here: {original_sentence}.",
        "'{keyword}' emerges as a key point, particularly in the context of: {original_sentence}.",
        "The text brings attention to '{keyword}' with this remark: {original_sentence}."
    ]

    for keyword in keywords:
        original_sentence = None
        for sentence in sentences:
            if keyword.lower() in sentence.lower():
                original_sentence = sentence
                break
        
        if keyword not in keyword_sentences:
            if original_sentence:
                template = choice(creative_templates)
                keyword_sentences[keyword] = template.format(keyword=keyword, original_sentence=original_sentence.lower())
            else:
                keyword_sentences[keyword] = f"The term '{keyword}' is significant but lacks direct context in the current text."

    return keyword_sentences


if __name__ == '__main__':
    file_path = "fisier.txt"
    output = read_from_file(file_path)
    print(output)
    print("---------------")
    
    my_text = make_string_from_list(output)
    if my_text and my_text.strip():
        language, probabilities = detect_language(my_text)
        print(f"lang: {language}")
        print(f"lang probs: {probabilities}")
    else:
        print("empty file, or contains only whitespaces")
        
    print("---------------")
    
    analysis = stylometric_analysis(my_text)
    print("\nStylometric Analysis:")
    print(f"Number of words: {analysis['word_count']}")
    print(f"Number of characters: {analysis['char_count']}")
    print(f"Number of unique words: {analysis['unique_words']}")
    print(f"Lexical density: {analysis['lexical_density']:.2f}")
    
    plot_word_frequencies(analysis['word_frequency'])
    
    print("---------------")
    
    alternative_text = generate_alternatives(my_text)
    print("Alternative Version of the Text:")
    print(alternative_text)
    
    print("---------------")
    
    keywords = extract_keywords_with_rake(my_text)
    print(f"keywords: {keywords}")
    
    with open('cuvinte-cheie.txt','w') as file:
        for keyword in keywords:
            file.write(keyword+'\n')
    
    print(f"First {keywords[0]}")
    
    print("---------------")
    
    keyword_sent = generate_sentences_from_keywords(keywords, my_text)
    
    print("Generated sentences for Keywords:")
    for keyword, sentence in keyword_sent.items():
        print(f"{keyword}: {sentence}")

    


    
    
