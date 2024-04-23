# Chain of Density Summarization Technique

This repository demonstrates the implementation of the Chain of Density method for text summarization, using Instructor to fine-tune a GPT-3.5 model. This approach mimics GPT-4's iterative summarization capabilities and substantially reduces latency and costs, while maintaining high entity density in summaries.

## Features
- **Iterative Summarization**: Apply the Chain of Density technique to create rich, detailed summaries.
- **Efficiency Gains**: Achieve up to 20x faster processing and 50x cost reduction compared to traditional GPT 4 zero shot prompting methods.
## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

![Static Badge](https://img.shields.io/badge/license-MIT-yellow)
![Static Badge](https://img.shields.io/badge/gpt3.5-8A2BE2)
![Static Badge](https://img.shields.io/badge/language-python-blue)

## Installation 

Clone the repo

```
git clone https://github.com/sanjaykmenon/cod
cd cod
```
Create a virtual environment
```
python -m venv venv
```
Activate virtual environment (in Windows)
```
.\venv\Scripts\activate 
```
Activate virtual environment (in macOS / Linux)
```
source venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```
Download Spacy Model
```
python -m spacy download en_core_web_sm
```
Run Locally
```
python chain_of_density_summary.py /path/to/your/pdf/document.pdf
```