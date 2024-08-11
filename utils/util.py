import requests
from bs4 import BeautifulSoup
import re



# get html from url 
def getTextFromURL(url):
  # Fetch the webpage content
  response = requests.get(url)
  #get response
  html = response.content
  return html


# Remove html tags using beautiful soup
def removeHTMLTags(html):
  soup = BeautifulSoup(html, 'html.parser')

  # Decompose the style and script tags
  for data in soup(['style', 'script']):
      data.decompose()

  # Return only the text
  return ' '.join(soup.stripped_strings)

# remove text not needed, by reducing the array 
def removeNotNeedeText(text, start, stop):

  #remove text before start
  index = text.find(start)

  if index != -1:
    text = text[index + len(start):]

  #remove text after stop
  index = text.find(stop)

  if index != -1:
    text = text[0:index]

  return text

# Remove url if has any 
def removeURL(text):
  # Define a regex pattern for matching URLs
  url_pattern = r'(https?:\/\/(?:www\.)?|www\.)[a-zA-Z0-9-._~:/?#\[\]@!$&\'()*+,;=]+'

  # Use re.sub to replace URLs with an empty string
  cleaned_text = re.sub(url_pattern, '', text)

  return cleaned_text



def obtainTextFromURL(url,newsChannel=''):
  print(url)
  #get txt from html
  html = getTextFromURL(url)

  #remove html tags
  noHTMLText = removeHTMLTags(html)

  #remove urls
  noHTMLText = removeURL(noHTMLText)

  if newsChannel == 'cp24':
    #reduce text base on news source, for cp24 the news end when the word Related Stories appear
    noHTMLText = removeNotNeedeText(noHTMLText, 'Last Updated' , 'Related Stories')
    noHTMLText = removeNotNeedeText(noHTMLText, 'Published' , 'Share:')
    noHTMLText = removeNotNeedeText(noHTMLText, 'EDT' , 'Share:')
    noHTMLText = removeNotNeedeText(noHTMLText, 'EDT' , 'Related Stories')

  elif newsChannel == 'citynews':
    #reduce text base on news source, for citynews the news end when the word Related Stories appear
    noHTMLText = removeNotNeedeText(noHTMLText, 'Last Updated' , 'Submit a Correction')
    noHTMLText = removeNotNeedeText(noHTMLText, 'Posted' , 'Submit a Correction')
    # Define the regex pattern to match date and time
    date_time_pattern = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|\d{1,2})(?:\s+\d{1,2},\s+\d{4}(?:\s+\d{1,2}:\d{2}\s*(?:am|pm))?)?\b'
    # Replace the matched pattern with an empty string
    noHTMLText = re.sub(date_time_pattern, '', noHTMLText)
  else: 
    noHTMLText = removeNotNeedeText(noHTMLText, 'Last Updated' , 'Related Stories')
    noHTMLText = removeNotNeedeText(noHTMLText, 'Published' , 'Share:')
    noHTMLText = removeNotNeedeText(noHTMLText, 'EDT' , 'Share:')
    noHTMLText = removeNotNeedeText(noHTMLText, 'EDT' , 'Related Stories')
    noHTMLText = removeNotNeedeText(noHTMLText, 'Last Updated' , 'Submit a Correction')
    noHTMLText = removeNotNeedeText(noHTMLText, 'Posted' , 'Submit a Correction')

  return noHTMLText
