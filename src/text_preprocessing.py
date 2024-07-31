import re

from emoji import demojize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from spacy import load
from string import punctuation
from unicodedata import normalize

pattern = re.compile(r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*")
def remove_url(text: str) -> str:
    '''
    Remove URLs from the text
    '''
    return pattern.sub('', text)

# mapping of non-standard characters to standard ones
CHAR_REPLACEMENTS = {
    '‘': "'",
    '’': "'",
    '“': '"',
    '”': '"',
    '–': '-',
    '—': '-',
    '…': '...',
    '\u00A0': ' ',
    '`': "'",
}
translation_table = str.maketrans(CHAR_REPLACEMENTS)
def normalize_text(text: str) -> str:
    '''
    Replace non-standard characters to standard ones
    '''
    text = normalize('NFKD', text)
    return text.translate(translation_table)

def remove_punctuation(text: str) -> str:
    '''
    Remove punctuation marks from the text
    '''
    exclude = punctuation
    return text.translate(str.maketrans(exclude, ' ' * len(exclude)))

# mapping of chat abbreviations with their full forms
CHAT_WORDS = {
    'afaik': 'as far as i know', 'afk': 'away from keyboard', 'asap': 'as soon as possible', 'atk': 'at the keyboard', 
    'atm': 'at the moment', 'a3': 'anytime, anywhere, anyplace', 'bak': 'back at keyboard', 'bbl': 'be back later', 
    'bbs': 'be back soon', 'bfn': 'bye for now', 'b4n': 'bye for now', 'brb': 'be right back', 'brt': 'be right there', 
    'btw': 'by the way', 'b4': 'before', 'cu': 'see you', 'cul8r': 'see you later', 'cya': 'see you',
    'faq': 'frequently asked questions', 'fc': 'fingers crossed', 'fwiw': "for what it's worth", 'fyi': 'for your information', 
    'gal': 'get a life', 'gg': 'good game', 'gn': 'good night', 'gmta': 'great minds think alike', 'gr8': 'great!', 'g9': 
    'genius', 'ic': 'i see', 'icq': 'i seek you (also a chat program)', 'ilu': 'i love you', 'imho': 'in my honest/humble opinion', 
    'imo': 'in my opinion', 'iow': 'in other words', 'irl': 'in real life', 'ldr': 'long distance relationship', 
    'lmao': 'laugh my ass off', 'lol': 'laughing out loud', 'ltns': 'long time no see', 'l8r': 'later', 
    'mte': 'my thoughts exactly', 'm8': 'mate', 'nrn': 'no reply necessary', 'oic': 'oh i see', 'pita': 
    'pain in the ass', 'prt': 'party', 'prw': 'parents are watching', 'qpsa': 'que pasa?', 'rofl': 'rolling on the floor laughing', 
    'roflol': 'rolling on the floor laughing out loud', 'rotflmao': 'rolling on the floor laughing my ass off', 'sk8': 'skate', 
    'stats': 'your sex and age', 'asl': 'age, sex, location', 'thx': 'thank you', 'ttfn': 'ta-ta for now', 'ttyl': 'talk to you later', 
    'u': 'you', 'u2': 'you too', 'u4e': 'yours for ever', 'wb': 'welcome back', 'wtf': 'what the fuck', 'wtg': 'way to go', 
    'wuf': 'where are you from?', 'w8': 'wait', '7k': 'sick:-d laugher', 'tfw': 'that feeling when', 'mfw': 'my face when', 
    'mrw': 'my reaction when', 'ifyp': 'i feel your pain', 'tntl': 'trying not to laugh', 'jk': 'just kidding', 'idc': 'i do not care', 
    'ily': 'i love you', 'imu': 'i miss you', 'adih': 'another day in hell', 'zzz': 'sleeping, bored, tired', 'wywh': 'wish you were here', 
    'time': 'tears in my eyes', 'bae': 'before anyone else', 'fimh': 'forever in my heart', 'bsaaw': 'big smile and a wink', 
    'bwl': 'bursting with laughter', 'bff': 'best friends forever', 'csl': "can't stop laughing", 'math': 'mathematics', "rn": "right now"
}
re_replace = re.compile(r'\b(' + '|'.join(re.escape(abbrev) for abbrev in CHAT_WORDS.keys()) + r')\b')
def chat_conversion(text: str) -> str:
    '''
    Convert common chat abbreviations to their full forms.
    '''
    return re_replace.sub(lambda x: CHAT_WORDS[x.group(1)], text)

STOPWORDS = stopwords.words('english')
pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in STOPWORDS) + r')\b')
def remove_stopwords(text: str) -> str:
    '''
    Remove the stopwords from the text, that account for little to no meaning in the text
    '''
    return pattern.sub('', text)

nlp = load("en_core_web_sm")
pattern = re.compile(r'^[a-zA-Z0-9]+$')
def tokenise(text: str) -> list[str]:
    '''
    Tokenise each word in the text
    '''
    doc = nlp(text)
    # filter out non english words 
    return list(filter(pattern.match, [s.text for s in doc]))

ps = PorterStemmer()
def stem_words(ls: list[str]) -> str:
    '''
    Stem each word to its root form.
    '''
    return ' '.join([ps.stem(word) for word in ls])


'''The processes to be applied on each document in the dataset'''
PROCESSES = (
            str.lower, remove_url, demojize, normalize_text, remove_punctuation, 
            chat_conversion, remove_stopwords, tokenise, stem_words
            )