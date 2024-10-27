from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import spacy
import en_core_web_sm
from collections import Counter

app = Flask(__name__)
CORS(app)

# Load spaCy model for text processing
nlp = spacy.load('en_core_web_sm')

# Load models
toxicity_classifier = pipeline("text-classification", model="unitary/toxic-bert", return_all_scores=True)

# Load semantic model
semantic_model_name = "roberta-base"
tokenizer = AutoTokenizer.from_pretrained(semantic_model_name)
semantic_model = AutoModelForSequenceClassification.from_pretrained(semantic_model_name, num_labels=3)

# Define microaggression categories (same as before)
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
    # ... (rest of categories remain the same)
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

def semantic_analysis(text):
    """Perform semantic analysis on text."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = semantic_model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probabilities[0].tolist()

@app.route('/analyze', methods=['POST'])
def analyze_text():
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'No text provided'}), 400
    
    text = request.json['text']
    
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
        'toxic_score': float(toxic_score if toxic_score else 0),
        'negative_score': float(negative_score),
        'is_microaggression': False,
        'reason': '',
        'categories': {}
    }
    
    # Check for microaggression
    if (toxic_score and toxic_score > 0.5) or negative_score > 0.7:
        results['is_microaggression'] = True
        results['categories'] = identify_categories(text)
        
        if toxic_score and toxic_score > 0.5:
            results['reason'] = "Microaggression detected due to toxicity!"
        else:
            results['reason'] = "Microaggression detected due to strong negative semantics!"
    else:
        results['reason'] = "No microaggression detected."
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
