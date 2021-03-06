from google.cloud import vision, language
from google.cloud.language import enums
from google.cloud.language import types
from random import choice
import six
import pprint

# magnitude words
weakList = ['weakly','lamely']
moderateList = ['moderately', 'sort of']
aggroList = ['aggressively', 'forcefully', 'strongly']
overList = ['intensely']

# positive/negative words
vBadList = ['miserable', 'agonizing', 'depressed']
badList = ['bad', 'negative', 'gloomy',]
neutralList = ['neutral', 'indifferent', 'apathetic']
posList = ['positive', 'good', 'favorable']
joyList = ['joyful', 'sublime', 'ecstatic']

def addMag(mag):
    """
    Based on a passed-in magnitude value, return a word from
    the appropriate list 
    """
    if (mag <= 0.1):
        return choice(weakList)
    elif (mag <= 0.35):
        return choice(moderateList)
    elif (mag <= 0.5):
        return choice(aggroList)
    else:
        return choice(overList)

def mapTextToEmotion(sentiment):
    """
    Given a Google NLP sentiment analysis, translate into human-readable 
    format with a modifier and an emotion
    """
    tone = []
    score = sentiment.score
    mag = sentiment.magnitude
    tone.append(addMag(mag))
    # very negative
    if score < -0.6:
        tone.append(choice(vBadList))
    # weakly negative
    elif score < -0.1:
        tone.append(choice(badList))
    # nuetral
    elif score < 0.1:
        tone.append(choice(neutralList))
    # weakly postiive
    elif score < 0.6:
        tone.append(choice(posList))
    # very positive
    else:
        tone.append(choice(joyList))
    return tone

def googleTextAnalysis(text):
    """
    Wrapper for the google NLP Sentiment Analysis API
    """
    client = language.LanguageServiceClient()
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT, language='en')
    sentiment = client.analyze_sentiment(document).document_sentiment
    return mapTextToEmotion(sentiment)

def googleImageAnalysis(url):
    """
    Wrapper for the google Vision image analysis API
    """
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = url
    response = client.label_detection(image=image)
    labels = response.label_annotations
    labelDesc = []
    for label in labels:
        labelDesc.append(label.description)
    return labelDesc