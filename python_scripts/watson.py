"""
    watson.py

    Connects to Watson Natural Language Classifier API.
"""

from watson_developer_cloud import NaturalLanguageClassifierV1

def get_illness(request):
    natural_language_classifier = NaturalLanguageClassifierV1(
      username='',
      password='')

    classes = natural_language_classifier.classify('', request)
    print(type(classes))
    return classes['classes']

