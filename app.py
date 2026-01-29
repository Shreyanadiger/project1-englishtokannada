from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Get port from environment variable or use 5000 as default
PORT = int(os.environ.get('PORT', 5000))

# Comprehensive English to Kannada Dictionary
KANNADA_DICTIONARY = {
    'hello': 'ನಮಸ್ಕಾರ',
    'hi': 'ನಮಸ್ಕಾರ',
    'goodbye': 'ವಿದಾಯ',
    'bye': 'ವಿದಾಯ',
    'good morning': 'ಶುಭೋದಯ',
    'good afternoon': 'ಶುಭ ಮಧ್ಯಾಹ್ನ',
    'good evening': 'ಶುಭ ಸಂಜೆ',
    'good night': 'ಶುಭರಾತ್ರಿ',
    'thank you': 'ಧನ್ಯವಾದ',
    'thanks': 'ಧನ್ಯವಾದ',
    'please': 'ದಯವಿಟ್ಟು',
    'yes': 'ಹೌದು',
    'no': 'ಇಲ್ಲ',
    'ok': 'ಸರಿ',
    'okay': 'ಸರಿ',
    'how are you': 'ನೀವು ಹೇಗಿದ್ದೀರಿ',
    'i am fine': 'ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ',
    'what is your name': 'ನಿಮ್ಮ ಹೆಸರೇನು',
    'my name is': 'ನನ್ನ ಹೆಸರು',
    'welcome': 'ಸ್ವಾಗತ',
    'sorry': 'ಕ್ಷಮೆ',
    'excuse me': 'ಕ್ಷಮೆ',
    'love': 'ಪ್ರೀತಿ',
    'friend': 'ಸ್ನೇಹಿತ',
    'family': 'ಕುಟುಂಬ',
    'water': 'ನೀರು',
    'food': 'ಆಹಾರ',
    'house': 'ಮನೆ',
    'mother': 'ತಾಯಿ',
    'father': 'ತಂದೆ',
    'brother': 'ಸಹೋದರ',
    'sister': 'ಸಹೋದರಿ',
    'son': 'ಮಗ',
    'daughter': 'ಹೆಣ್ಣು',
    'wife': 'ಪತ್ನಿ',
    'husband': 'ಪತಿ',
    'love you': 'ನಿನ್ನನ್ನು ಪ್ರೀತಿಸುತ್ತೇನೆ',
    'good': 'ಉತ್ತಮ',
    'bad': 'ಕೆಟ್ಟ',
    'beautiful': 'ಸುಂದರ',
    'happy': 'ಸುಖಿ',
    'sad': 'ದುಃಖಿ',
    'angry': 'ಕೋಪಿ',
    'tired': 'ಆಲಸ್ಯ',
    'help': 'ಸಹಾಯ',
    'thank you so much': 'ತುಂಬಾ ಧನ್ಯವಾದ',
    'how much': 'ಎಷ್ಟು',
    'how many': 'ಎಷ್ಟು',
    'where': 'ಎಲ್ಲಿ',
    'when': 'ಯಾವಾಗ',
    'what': 'ಏನು',
    'why': 'ಏಕೆ',
    'who': 'ಯಾರು',
    'today': 'ಇಂದು',
    'tomorrow': 'ನಾಳೆ',
    'yesterday': 'ನಿನ್ನೆ',
    'morning': 'ಬೆಳಿಗ್ಗೆ',
    'evening': 'ಸಂಜೆ',
    'night': 'ರಾತ್ರಿ',
    'school': 'ಶಾಲೆ',
    'college': 'ಕಾಲೇಜು',
    'office': 'ಕಛೇರಿ',
    'hospital': 'ಆಸ್ಪತ್ರೆ',
    'market': 'ಮಾರುಕಟ್ಟೆ',
    'park': 'ಪಾರ್ಕ್',
    'beach': 'ಸಮುದ್ರ ತೀರ',
    'mountain': 'ಬೆಟ್ಟ',
    'river': 'ನದಿ',
    'tree': 'ಮರ',
    'flower': 'ಪುಷ್ಪ',
    'animal': 'ಪ್ರಾಣಿ',
    'dog': 'ನಾಯಿ',
    'cat': 'ಬಿಲ್ಲಿ',
    'bird': 'ಪಕ್ಷಿ',
    'fish': 'ಮೀನು',
    'elephant': 'ಆನೆ',
    'lion': 'ಸಿಂಹ',
    'tiger': 'ಹುಲಿ',
    'color': 'ಬಣ್ಣ',
    'red': 'ಕೆಂಪು',
    'blue': 'ನೀಲಿ',
    'green': 'ಹಸಿರು',
    'yellow': 'ಹಳದಿ',
    'black': 'ಕಪ್ಪು',
    'white': 'ಬಿಳುಪು',
    'one': 'ಒಂದು',
    'two': 'ಎರಡು',
    'three': 'ಮೂರು',
    'four': 'ನಾಲ್ಕು',
    'five': 'ಐದು',
    'six': 'ಆರು',
    'seven': 'ಏಳು',
    'eight': 'ಎಂಟು',
    'nine': 'ಒಂಬತ್ತು',
    'ten': 'ಹತ್ತು',
    'please help me': 'ದಯವಿಟ್ಟು ನನಗೆ ಸಹಾಯ ಮಾಡಿ',
    'what time is it': 'ಇದು ಯಾವ ಸಮಯ',
    'where is the bathroom': 'ಟಾಯ್ಲೆಟ್ ಎಲ್ಲಿದೆ',
    'can you help me': 'ನೀವು ನನಗೆ ಸಹಾಯ ಮಾಡುವಿರಾ',
    'i do not understand': 'ನನಗೆ ತಿಳಿದಿಲ್ಲ',
    'speak slowly': 'ನಿಧಾನವಾಗಿ ಮಾತನಾಡಿ',
    'do you speak english': 'ನೀವು ಇಂಗ್ಲಿಷ್ ಮಾತನಾಡುತ್ತೀರಾ'
}

def text_to_speech(text, language='en'):
    """
    Note: Speech synthesis is now handled by browser Web Speech API
    This function is kept for backward compatibility if needed
    """
    pass

def translate_english_to_kannada(text):
    """
    Translates English text to Kannada
    First tries dictionary lookup, then API fallback
    """
    text_lower = text.lower().strip()
    
    # Try exact match in dictionary first
    if text_lower in KANNADA_DICTIONARY:
        return KANNADA_DICTIONARY[text_lower]
    
    # Try API for sentences or words not in dictionary
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': 'en|kn'
        }
        response = requests.get(url, params=params, timeout=5)
        result = response.json()
        
        if result['responseStatus'] == 200:
            api_translation = result['responseData']['translatedText']
            if api_translation and api_translation != text:
                return api_translation
    except Exception as e:
        print(f"API Error: {str(e)}")
    
    # If not found, return the text as is
    return text

@app.route('/')
def home():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """API endpoint for translation"""
    try:
        data = request.get_json()
        english_text = data.get('text', '').strip()
        
        if not english_text:
            return jsonify({
                'success': False,
                'error': 'Please enter some text!'
            }), 400
        
        kannada_text = translate_english_to_kannada(english_text)
        
        return jsonify({
            'success': True,
            'kannada_text': kannada_text
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/speak-english', methods=['POST'])
def speak_english():
    """Speech synthesis is now handled by browser Web Speech API"""
    return jsonify({'success': True, 'message': 'Use browser speech API'}), 200

@app.route('/speak-kannada', methods=['POST'])
def speak_kannada():
    """Speech synthesis is now handled by browser Web Speech API"""
    return jsonify({'success': True, 'message': 'Use browser speech API'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=PORT)
