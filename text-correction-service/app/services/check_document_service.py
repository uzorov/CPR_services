from fastapi import Depends

import re
from autocorrect import Speller
from nltk.tokenize import word_tokenize, sent_tokenize

from app.sage.sage.spelling_correction import T5ModelForSpellingCorruption, RuM2M100ModelForSpellingCorrection, \
    AvailableCorrectors

spell = Speller(lang='ru', fast=True)

model_fast = (T5ModelForSpellingCorruption
              .from_pretrained(AvailableCorrectors
                               .sage_fredt5_distilled_95m
                               .value))

# model_long = (RuM2M100ModelForSpellingCorrection.from_pretrained(
#     AvailableCorrectors.sage_m2m100_1B.value
# ))


class CheckDocumentService:

    def correct_text_using_ai_fast(self, text: str) -> str:
        words = word_tokenize(text)
        new_words = []
        for i in range(len(words)):
            if i == 0 or words[i].lower() != words[i - 1].lower():
                new_words.append(words[i])
        text = ' '.join(new_words)
        corrected_text = model_fast.correct(text)
        print("fast ai ", corrected_text)
        return corrected_text

    def correct_text_using_ai_long(self, text: str) -> str:
        words = word_tokenize(text)
        new_words = []
        for i in range(len(words)):
            if i == 0 or words[i].lower() != words[i - 1].lower():
                new_words.append(words[i])
        text = ' '.join(new_words)
        corrected_text = model_long.correct(text)
        print("long ai ", corrected_text)
        return corrected_text

    def correct_text_using_algorithm(self, text: str) -> str:
        # Опечатки и правописание через дефис

        corrected_text = spell(text)
        # Лишние пробелы
        corrected_text = re.sub(r'\s+', ' ', corrected_text).strip()

        # Повтор слов
        words = word_tokenize(corrected_text)
        new_words = []
        for i in range(len(words)):
            if i == 0 or words[i].lower() != words[i - 1].lower():
                new_words.append(words[i])
        corrected_text = ' '.join(new_words)

        # Строчная буква в начале предложения
        sentences = sent_tokenize(corrected_text)
        sentences = [sentence.capitalize() for sentence in sentences]
        corrected_text = ' '.join(sentences)

        # Непарные скобки и апострофы
        def fix_unpaired_symbols(text, symbol):
            count_open = text.count(symbol[0])
            count_close = text.count(symbol[1])
            if count_open > count_close:
                text += symbol[1] * (count_open - count_close)
            elif count_close > count_open:
                text = symbol[0] * (count_close - count_open) + text
            return text

        corrected_text = fix_unpaired_symbols(corrected_text, ('(', ')'))
        corrected_text = fix_unpaired_symbols(corrected_text, ('[', ']'))
        corrected_text = fix_unpaired_symbols(corrected_text, ('{', '}'))
        corrected_text = fix_unpaired_symbols(corrected_text, ("'", "'"))
        corrected_text = fix_unpaired_symbols(corrected_text, ('"', '"'))

        # Выделение запятыми вводных слов
        intro_words = ['например', 'однако', 'кстати', 'во-первых', 'во-вторых', 'в-третьих']
        for word in intro_words:
            corrected_text = re.sub(r'\b ' + word + r'\b', f', {word},', corrected_text)
        intro_words = ['Например', 'Однако', 'Кстати', 'Во-первых', 'Во-вторых', 'В-третьих']
        for word in intro_words:
            corrected_text = re.sub(r'\b' + word + r'\b', f'{word},', corrected_text)

        # Две запятые или точки подряд
        corrected_text = re.sub(r',,', ',', corrected_text)
        corrected_text = re.sub(r',,', ',', corrected_text)
        corrected_text = re.sub(r'\.\.', '.', corrected_text)
        corrected_text = re.sub(r' , ', ', ', corrected_text)
        corrected_text = re.sub('\( ', '(', corrected_text)
        corrected_text = re.sub(' \)', ')', corrected_text)

        return corrected_text
