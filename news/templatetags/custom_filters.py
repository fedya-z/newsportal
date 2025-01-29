from django import template

register = template.Library()

BANNED_WORDS = []
@register.filter()
def censor(text):
    for word in BANNED_WORDS:
        censored_word = '*' * len(word)
        text = text.replace(word, censored_word)
    return text
