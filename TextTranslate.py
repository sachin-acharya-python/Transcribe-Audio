from googletrans import Translator, constants
from googletrans.models import Translated
from pprint import pprint

translator = Translator()

def tranlate(text: str | list[str], dest: str = "en", src: str = 'auto') -> (list | Translated):
    translations = translator.translate(text, dest=dest, src=src)
    if not isinstance(translations, list):
        translations = [translations]

    for translation in translations:
        print(f"{translation.origin} ({translation.src}) -> {translation.text} ({translation.dest})")
    return translations


text = ["Hello Everyone", "How are you?"]
dest = "tr"

tranlate(text, dest)