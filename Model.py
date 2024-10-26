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
        # Female-related terms
        'woman', 'girl', 'female', 'lady', 'mother', 'emotional', 'hormonal',
        'hysteric', 'feminine', 'secretary', 'nurse', 'bossy',
        # Male-related terms
        'man', 'boy', 'male', 'gentleman', 'father', 'aggressive', 'masculine',
        'macho', 'tough', 'sissy', 'weak', 'provider', 'breadwinner',
        # General gender terms
        'gender', 'sex', 'transgender', 'identity', 'role', 'stereotype',
        'patriarchy', 'feminism', 'toxic', 'equality'
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

# Define severity thresholds
SEVERITY_THRESHOLDS = {
    'no_microaggression': {
        'toxic_score': 0.3,
        'negative_score': 0.4
    },
    'moderate': {
        'toxic_score': 0.6,
        'negative_score': 0.7
    }
    # Anything above these thresholds is considered peak toxicity
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

def determine_severity(toxic_score, negative_score):
    """Determine the severity level of the microaggression."""
    if toxic_score <= SEVERITY_THRESHOLDS['no_microaggression']['toxic_score'] and \
       negative_score <= SEVERITY_THRESHOLDS['no_microaggression']['negative_score']:
        return "no_microaggression"
    elif toxic_score <= SEVERITY_THRESHOLDS['moderate']['toxic_score'] and \
         negative_score <= SEVERITY_THRESHOLDS['moderate']['negative_score']:
        return "moderate"
    else:
        return "peak_toxicity"

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
    
    # Determine severity
    severity = determine_severity(toxic_score if toxic_score else 0, negative_score)
    
    results = {
        'toxic_score': toxic_score if toxic_score else 0,
        'negative_score': negative_score,
        'severity': severity,
        'categories': {},
        'reason': ''
    }
    
    # Set reason and identify categories based on severity
    if severity == "no_microaggression":
        results['reason'] = "No microaggression detected."
    elif severity == "moderate":
        results['reason'] = "Moderate microaggression detected!"
        results['categories'] = identify_categories(text)
    else:  # peak_toxicity
        results['reason'] = "⚠️  Peak toxicity detected! Strong microaggression present!"
        results['categories'] = identify_categories(text)
    
    # Get word contributions and generate word cloud
    word_scores = get_token_contributions(text, results)
    generate_wordcloud(word_scores)
    
    return results

def main():
    print("Enhanced Microaggression Detection System with Three-Level Classification")
    print("----------------------------------------------------------------------")
    print("\nSeverity Levels:")
    print("1. No Microaggression: Safe content")
    print("2. Moderate: Potentially problematic content")
    print("3. Peak Toxicity: Highly problematic content")
    
    while True:
        user_input = input("\nEnter a sentence to analyze (or type 'exit' to stop): ")
        if user_input.lower() == 'exit':
            break
        
        results = detect_microaggression(user_input)
        print(f"\nAnalysis Results:")
        print(f"- Severity: {results['severity'].replace('_', ' ').title()}")
        print(f"- {results['reason']}")
        print(f"- Toxicity Score: {results['toxic_score']:.3f}")
        print(f"- Negative Sentiment Score: {results['negative_score']:.3f}")
        
        # Only display categories for moderate and peak toxicity
        if results['severity'] != "no_microaggression" and results['categories']:
            print("\nDetected Categories:")
            for category, details in results['categories'].items():
                print(f"- {category.title()}:")
                print(f"  Confidence: {details['confidence']:.2f}")
                print(f"  Matching terms: {', '.join(details['matching_terms'])}")

if __name__ == "__main__":
    main()