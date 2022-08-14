import pyjokes
from googletrans import Translator

translator = Translator()

def getJoke():
    """
    Description:
        Get a random joke.

    Returns:
        - joke.text: The joke
    """

    en_joke = pyjokes.get_joke()
    joke = translator.translate(en_joke, src="en", dest="de")
    print(f"[INFO-intelligenceDampeningCore/getJoke] A joke has been generated.")
    return (joke.text)