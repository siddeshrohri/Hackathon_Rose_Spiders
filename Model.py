from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import spacy
import en_core_web_sm

# Load spaCy model for text processing
nlp = spacy.load('en_core_web_sm')

# Load models
toxicity_classifier = pipeline("text-classification", model="unitary/toxic-bert", return_all_scores=True)

# Load semantic model
semantic_model_name = "roberta-base"
tokenizer = AutoTokenizer.from_pretrained(semantic_model_name)
semantic_model = AutoModelForSequenceClassification.from_pretrained(semantic_model_name, num_labels=3)

# Define microaggression categories and their associated keywords
MICROAGGRESSION_CATEGORIES = {
    'racism': [
        'ethnic', 'racial', 'culture', 'minority', 'foreign', 'immigrant', 'accent',
        'asian', 'black', 'white', 'latino', 'hispanic', 'indian', 'native',
        'exotic', 'ghetto', 'thug', 'articulate', 'civilized'
    ],
    'sexism': [
        'woman', 'girl', 'female', 'lady', 'mother', 'emotional', 'hormonal',
        'hysteric', 'boss lady', 'masculine', 'feminine', 'gender', 'secretary',
        'nurse', 'bossy', 'aggressive'
    ],
    'ageism': [
        'old', 'young', 'boomer', 'millennial', 'senior', 'elderly', 'kid',
        'mature', 'experienced', 'retirement', 'generation', 'age', 'dated'
    ],
    'ableism': [
        'disabled', 'handicapped', 'blind', 'deaf', 'dumb', 'crazy', 'insane',
        'mental', 'special', 'normal', 'retarded', 'wheelchair', 'condition'
    ],
    'classism': [
        'poor', 'rich', 'wealthy', 'welfare', 'educated', 'fancy', 'privileged',
        'hood', 'classy', 'expensive', 'cheap', 'quality', 'afford'
    ],
    'xenophobia': [
        'immigrant', 'foreigner', 'alien', 'illegal', 'citizen', 'passport',
        'accent', 'country', 'nation', 'american', 'english', 'homeland'
    ]
}

def preprocess_text(text):
    """Process text to extract meaningful words."""
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct 
             and token.pos_ in ['ADJ', 'VERB', 'NOUN', 'ADV']]
    return tokens

def identify_categories(text):
    """Identify potential microaggression categories based on keywords."""
    text_lower = text.lower()
    tokens = set(preprocess_text(text))
    
    categories = {}
    for category, keywords in MICROAGGRESSION_CATEGORIES.items():
        matches = tokens.intersection(set(keywords))
        if matches:
            # Calculate a confidence score based on number of matching keywords
            confidence = len(matches) / len(tokens)
            if confidence > 0.1:
                categories[category] = {
                    'confidence': confidence,
                    'matching_terms': list(matches)
                }
    
    return categories

def get_token_contributions(text, model_outputs):
    """Get word contributions to negative sentiment."""
    tokens = preprocess_text(text)
    
    word_scores = Counter(tokens)
    
    toxic_score = model_outputs['toxic_score']
    negative_score = model_outputs['negative_score']
    
    for word in word_scores:
        word_scores[word] *= (toxic_score + negative_score) / 2
    
    return dict(word_scores)

def generate_wordcloud(word_scores):
    """Generate and display word cloud from word scores."""
    if not word_scores:
        print("No significant negative words detected.")
        return
    
    wordcloud = WordCloud(
        width=800, 
        height=400,
        background_color='white',
        colormap='Reds'
    ).generate_from_frequencies(word_scores)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Words Contributing to Negative Detection')
    plt.show()

def semantic_analysis(text):
    """Perform semantic analysis on text."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = semantic_model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probabilities[0].tolist()

def detect_microaggression(text):
    """Detect microaggression and return detailed analysis."""
    # Get predictions from toxicity classifier
    toxicity_predictions = toxicity_classifier(text)
    toxic_score = None
    for label in toxicity_predictions[0]:
        if label['label'] == 'toxic':
            toxic_score = label['score']
            break
    
    # Get semantic analysis scores
    semantic_scores = semantic_analysis(text)
    neutral_score = semantic_scores[0]
    positive_score = semantic_scores[1]
    negative_score = semantic_scores[2]
    
    # Initialize results
    results = {
        'toxic_score': toxic_score if toxic_score else 0,
        'negative_score': negative_score,
        'is_microaggression': False,
        'reason': '',
        'categories': {}  # Initialize empty categories
    }
    
    # Only identify categories if toxicity or strong negative sentiment is detected
    if (toxic_score and toxic_score > 0.5) or negative_score > 0.7:
        results['is_microaggression'] = True
        results['categories'] = identify_categories(text)
        
        if toxic_score and toxic_score > 0.5:
            results['reason'] = "Microaggression detected due to toxicity!"
        else:
            results['reason'] = "Microaggression detected due to strong negative semantics!"
    else:
        results['reason'] = "No microaggression detected."
    
    # Get word contributions and generate word cloud
    word_scores = get_token_contributions(text, results)
    generate_wordcloud(word_scores)
    
    return results

def main():
    print("Enhanced Microaggression Detection System with Word Cloud Visualization")
    print("------------------------------------------------------------------")
    while True:
        user_input = input("\nEnter a sentence to analyze (or type 'exit' to stop): ")
        if user_input.lower() == 'exit':
            break
        
        results = detect_microaggression(user_input)
        print(f"\nAnalysis Results:")
        print(f"- {results['reason']}")
        print(f"- Toxicity Score: {results['toxic_score']:.3f}")
        print(f"- Negative Sentiment Score: {results['negative_score']:.3f}")
        
        # Only display categories if microaggression is detected
        if results['is_microaggression'] and results['categories']:
            print("\nDetected Categories:")
            for category, details in results['categories'].items():
                print(f"- {category.title()}:")
                print(f"  Confidence: {details['confidence']:.2f}")
                print(f"  Matching terms: {', '.join(details['matching_terms'])}")
        elif results['is_microaggression'] and not results['categories']:
            print("\nNo specific category identified, but content is potentially harmful.")

if __name__ == "__main__":
    main()