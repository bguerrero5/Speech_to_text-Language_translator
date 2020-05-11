from ibm_watson import SpeechToTextV1, LanguageTranslatorV3
from pandas import json_normalize
import numpy as np
import json
import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from settings import SPEECH_API_KEY, SPEECH_IAM_APIKEY, SPEECH_URL, SPEECH_AUTH_TYPE, LT_API_KEY, LT_IAM_APIKEY, LT_URL, LT_AUTH_TYPE

# Authentication process for IBM Speech to Text API service.
s2t_authenticator = IAMAuthenticator(SPEECH_API_KEY)
speech_to_text = SpeechToTextV1(authenticator=s2t_authenticator)
speech_to_text.set_service_url(SPEECH_URL)


def ibm_s2t(audio_file):
    """
    Requesting the IBM Speech to Text Api to recognize the text of an audio file.
    Cleaning the api response to save all the regonized text into a variable called finished_text.
    """
    print()
    print("we are currently analyzing the audio file you provided. this should take a moment...".upper())
    with open(audio_file, mode="rb") as wav:
        response = speech_to_text.recognize(
            audio=wav, content_type="audio/mp3")
        i = 0
        recognized_text = []
        for i in range(len(response.result["results"])):
            recognized_text.append(response.result["results"][i]["alternatives"][0]["transcript"])
            finished_text= " ".join(recognized_text)

    print()
    print(f"This is the {audio_lang} text we found in the audio file provided.".upper())
    print()
    print(finished_text)
    print()
    return finished_text


# Authentication process for IBM Languate Transaltio API service.

lt_authenticator = IAMAuthenticator(LT_API_KEY)
version_lt = "2018-05-01"
language_translator = LanguageTranslatorV3(
    version=version_lt, authenticator=lt_authenticator)
language_translator.set_service_url(LT_URL)
language_translator

def language_check():
    """
    Requests user to input the language in the audio file. Correlates the input language in the data
    IBM Language Transalte API service to see if language is available. Request user for the translation language.
    If both exist lanaugages exist in IBM Language Transalte API service, process continues. Else, no translation is possible.
    """
    print()
    global audio_lang
    audio_lang = input(str("Please input the language in the audio file (input language): " )).capitalize()
    print()
    global translation_lang
    translation_lang = input(str("Please input the lanague you want to translate to (output language): ")).capitalize()
    languages = json_normalize(language_translator.list_identifiable_languages().get_result(), "languages")
    np_languages = languages.to_numpy()
    try:
        if audio_lang in np_languages and translation_lang in np_languages:
            input_lang = np.where(np_languages == audio_lang)
            output_lang = np.where(np_languages == translation_lang)
            in_language = np_languages[input_lang[0][0]]
            out_language = np_languages[output_lang[0][0]]
            in_lang = in_language[0]
            out_lang = out_language[0]
            destination = in_lang + "-" + out_lang
            return destination
        else:
            print("Translation is not possible, input or output language not available.")
    except Exception as exc:
        print(exc)


def translate(audio_file):
    """
    Runs all the process needed for the proper speech to text translation.
    """
    destination = language_check()
    source_text = ibm_s2t(audio_file)
    ibm_translate(source_text, destination)


def ibm_translate(source_text, destination):
    """
    Requesting the IBM Language Translator API for a list of languages available. And Translating the recognized text
    from the audio file into the desired language. in this case English to Spanish.
    """
    rtext = source_text

    json_normalize(
        language_translator.list_identifiable_languages().get_result(), "languages")
    translation_response = language_translator.translate(
        text=rtext, model_id=destination)
    translation = translation_response.get_result()
    spanish_translation = translation["translations"][0]["translation"]

    # printing final product
    print(f"This is the text translation for your desired languange: {translation_lang}".upper())
    print()
    print(spanish_translation)
