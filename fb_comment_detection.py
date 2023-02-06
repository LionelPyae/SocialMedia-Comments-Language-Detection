from langdetect import detect, detect_langs
from langdetect import DetectorFactory
from pycountry import languages
from facebook import GraphAPI

class LanguageDetector:
  def __init__(self, access_token, post_id, emojis = ['💕', '👍'], method = "single"):
    self.access_token = access_token
    self.post_id = post_id
    self.emojis = emojis
    self.method = method
    self.graph = GraphAPI(self.access_token, version = 2.8)
    self.raw_comments = self.graph.get_object(id = self.post_id, fields='comments')
    self.comments = [comment['message'] for comment in self.raw_comments['comments']['data']]

  def language_detection(self, text):
    """
    @desc: 
      - detects the language of a text
    @params:
      - text: the text which language needs to be detected
    @return:
      - the langue/list of languages
    """
    DetectorFactory.seed = 0
    try:
      if(self.method.lower() != "single"):
        result = detect_langs(text)
      else:
        result = detect(text)
    except:
      return 'wrong'

    return result

  def run(self):
    for comment in self.comments:
      if isinstance(comment, (str, int)) and not any(c in comment for c in self.emojis):
        language_code = self.language_detection(comment)
        print(f'"{comment}" is written in {language_code} language')

access_token = 'EAANjMLpRZB9gBAD1iCIS6PZBdZBRebVnPIkzAwADqvNIo4z4rZBto1MIQpYbla0lHZBsZBQHwaAtwOvoZBq6M5xyGBRNY2HJmmsZBGEvBzF4IA85FfO8kCaBP3cAil1aFm5vjSygMXrzGiUkZBWGUWUbxgXsqLJThGAvvZAAWRePQZAhnHZCOpgaGyab98RnZBUwTfjQRVjvMMrFRl7a531xpq58CiZAikyN2F1ygZD'
post_id = '106238685563607_146314891555986'
emojis = ['💕', '👍']

detector = LanguageDetector(access_token, post_id, emojis)
detector.run()
