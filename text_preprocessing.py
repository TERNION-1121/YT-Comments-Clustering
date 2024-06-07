import re
from string import punctuation
from textblob import TextBlob
from nltk.corpus import stopwords


def remove_url(text: str):
    '''
    '''
    pattern = re.compile(r'https?://\S+|www\.\S+')
    return pattern.sub(r'', text)

def remove_punctuation(text: str):
    '''
    '''
    exclude = punctuation
    return text.translate(str.maketrans('', '', exclude))

CHAT_WORDS = {
    "AFAIK": "as far as i know",
    "AFK": "away from keyboard",
    "ASAP": "as soon as possible",
    "ATK": "at the keyboard",
    "ATM": "at the moment",
    "A3": "anytime, anywhere, anyplace",
    "BAK": "back at keyboard",
    "BBL": "be back later",
    "BBS": "be back soon",
    "BFN": "bye for now",
    "B4N": "bye for now",
    "BRB": "be right back",
    "BRT": "be right there",
    "BTW": "by the way",
    "B4": "before",
    "CU": "see you",
    "CUL8R": "see you later",
    "CYA": "see you",
    "FAQ": "frequently asked questions",
    "FC": "fingers crossed",
    "FWIW": "for what it's worth",
    "FYI": "for your information",
    "GAL": "get a life",
    "GG": "good game",
    "GN": "good night",
    "GMTA": "great minds think alike",
    "GR8": "great!",
    "G9": "genius",
    "IC": "i see",
    "ICQ": "i seek you (also a chat program)",
    "ILU": "i love you",
    "IMHO": "in my honest/humble opinion",
    "IMO": "in my opinion",
    "IOW": "in other words",
    "IRL": "in real life",
    "KISS": "keep it simple, stupid",
    "LDR": "long distance relationship",
    "LMAO": "laugh my ass off",
    "LOL": "laughing out loud",
    "LTNS": "long time no see",
    "L8R": "later",
    "MTE": "my thoughts exactly",
    "M8": "mate",
    "NRN": "no reply necessary",
    "OIC": "oh i see",
    "PITA": "pain in the ass",
    "PRT": "party",
    "PRW": "parents are watching",
    "QPSA": "que pasa?",
    "ROFL": "rolling on the floor laughing",
    "ROFLOL": "rolling on the floor laughing out loud",
    "ROTFLMAO": "rolling on the floor laughing my ass off",
    "SK8": "skate",
    "STATS": "your sex and age",
    "ASL": "age, sex, location",
    "THX": "thank you",
    "TTFN": "ta-ta for now!",
    "TTYL": "talk to you later",
    "U": "you",
    "U2": "you too",
    "U4E": "yours for ever",
    "WB": "welcome back",
    "WTF": "what the fuck",
    "WTG": "way to go!",
    "WUF": "where are you from?",
    "W8": "wait...",
    "7K": "sick:-d laugher",
    "TFW": "that feeling when",
    "MFW": "my face when",
    "MRW": "my reaction when",
    "IFYP": "i feel your pain",
    "TNTL": "trying not to laugh",
    "JK": "just kidding",
    "IDC": "i don't care",
    "ILY": "i love you",
    "IMU": "i miss you",
    "ADIH": "another day in hell",
    "ZZZ": "sleeping, bored, tired",
    "WYWH": "wish you were here",
    "TIME": "tears in my eyes",
    "BAE": "before anyone else",
    "FIMH": "forever in my heart",
    "BSAAW": "big smile and a wink",
    "BWL": "bursting with laughter",
    "BFF": "best friends forever",
    "CSL": "can't stop laughing"
}
def chat_conversion(text: str):
    '''
    '''
    text = text.split()
    for i in range(len(text)):
        if text[i].upper() not in CHAT_WORDS:
            continue
        text[i] = CHAT_WORDS[text[i].upper()]
    return ' '.join(text)
 
def correct_text(text: str):
    '''
    '''
    textBlb = TextBlob(text)
    return textBlb.correct().string

STOPWORDS = stopwords.words('english')
def remove_stopwords(text: str):
    '''
    '''
    words = text.split()
    for i in range(len(words)):
        if words[i] not in STOPWORDS:
            continue
        words[i] = ''
    return ' '.join(words)


PROCESSES = [str.lower, remove_url, remove_punctuation, chat_conversion, correct_text, remove_stopwords]