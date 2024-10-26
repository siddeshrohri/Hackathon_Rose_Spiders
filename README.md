# Hackathon_Rose_Spiders

## Overview
The Hackathon_Rose_Spiders project implements a microaggression detection system that leverages natural language processing (NLP) techniques to analyze text inputs. This system identifies potential microaggressions, visualizes the words contributing to negative sentiment, and provides detailed feedback on identified categories.

## Features
- **Microaggression Detection**: Analyzes text for signs of microaggressions across multiple categories.
- **Word Cloud Visualization**: Displays significant words contributing to negative sentiment in a visually appealing format.
- **Detailed Analysis**: Provides confidence scores and matching keywords for detected microaggressions.

## Requirements
The project requires several Python libraries. A `requirements.txt` file is provided to facilitate easy installation of these dependencies.

## Getting Started

### Prerequisites
Ensure you have Python 3.7 or higher installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

### Cloning the Repository
To get a local copy of this repository, use the following command:

```bash
git clone https://github.com/your-username/Hackathon_Rose_Spiders.git
```

### Installing the dependencies
Navigate to the project directory and install the required packages using pip:
```bash
pip install -r requirements.txt
```
### Downloading the SpaCy Model
You need to download the en_core_web_sm model for spaCy. You can do this by running:
```bash
python -m spacy download en_core_web_sm
```
### Running the Script
Once the dependencies are installed and the spaCy model is downloaded, you can run the main script using the following command:
```bash
python Models.py
```
