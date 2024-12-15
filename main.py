from collections import Counter
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from googletrans import Translator

translator = Translator()

# def summerizer(rawdoc):
#   stopwords = list(STOP_WORDS)
#
#   nlp=spacy.load('en_core_web_sm')
#   doc=nlp(rawdoc)
#   #print(doc)
#
#   tokens = [token.text for token in doc]
#   print(tokens)
#   word_frequencies = Counter(tokens)
#
#   keywords = nlargest(10, word_frequencies, key=word_frequencies.get)
#
#   word_frequencies = {}
#   for word in doc:
#     if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
#       if word.text not in word_frequencies.keys():
#         word_frequencies[word.text] = 1
#       else:
#         word_frequencies[word.text] += 1
#
#   #print(word_frequencies)
#
#   max_freq = max(word_frequencies.values())
#   #print(max_freq)
#
#   for word in word_frequencies.keys():
#     word_frequencies[word] = (word_frequencies[word]/max_freq)
#   #print(word_frequencies)
#
#   sent_tokens = [sent for sent in doc.sents]
#   #print(sent_tokens)
#
#   sent_scores = {}
#   for sent in sent_tokens:
#     for word in sent:
#       if word.text in word_frequencies.keys():
#         if sent not in sent_scores.keys():
#           sent_scores[sent] = word_frequencies[word.text]
#         else:
#           sent_scores[sent] += word_frequencies[word.text]
#   #print(sent_scores)
#
#   select_length = int(len(sent_tokens) * 0.3)
#   #print(select_length)
#
#   summary = nlargest(select_length, sent_scores.items(), key=lambda x: x[1])
#   final_summary = [sent.text for sent, score in summary]
#   summary = ' '.join(final_summary)
#
#   #print(summary)
#
#   final_summary = [sent.text for sent in summary]
#   summary = ' '.join(final_summary)
#   print(rawdoc)
#   print(summary)
#   print("original text",len(rawdoc.split(' ')))
#   print("summerized text",len(summary.split(' ')))
#
#   return summary,keywords,doc,len(rawdoc.split(' ')), len(summary.split(' '))

def summerizer(rawdoc):
  stopwords = list(STOP_WORDS)

  nlp = spacy.load('en_core_web_sm')
  doc = nlp(rawdoc)

  tokens = [token.text for token in doc]
  word_frequencies = Counter(tokens)

  word_frequencies = {}
  for word in doc:
    if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
      if word.text not in word_frequencies.keys():
        word_frequencies[word.text] = 1
      else:
        word_frequencies[word.text] += 1

  max_freq = max(word_frequencies.values())

  for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word] / max_freq)

  sent_tokens = [sent for sent in doc.sents]

  sent_scores = {}
  for sent in sent_tokens:
    for word in sent:
      if word.text in word_frequencies.keys():
        if sent not in sent_scores.keys():
          sent_scores[sent] = word_frequencies[word.text]
        else:
          sent_scores[sent] += word_frequencies[word.text]

  select_length = int(len(sent_tokens) * 0.3)

  summary = nlargest(select_length, sent_scores, key=sent_scores.get)

  # Fix here: Extract the text of each sentence in the summary
  final_summary = [sent.text for sent in summary]
  summary = ' '.join(final_summary)

  print("Original text:", len(rawdoc.split(' ')))
  print("Summarized text:", len(summary.split(' ')))

  return summary, tokens, doc, len(rawdoc.split(' ')), len(summary.split(' '))


def translate_summary(summary, target_language):
  try:
    # Debug logs
    print(f"Text to translate: {summary}")
    print(f"Target language: {target_language}")

    # Perform translation
    translated = translator.translate(summary, dest=target_language)
    print(f"Translated text: {translated.text}")

    return translated.text
  except Exception as e:
    print("Error in translation:", str(e))
    return "Translation failed. Please try again."
