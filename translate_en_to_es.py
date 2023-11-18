import pathlib
import glob
import json
import os

import argostranslate.package
import argostranslate.translate

from pprint import pprint
from translate import Translator
# from PyDictionary import PyDictionary 
from PyMultiDictionary import MultiDictionary

def download_and_install_package(from_code, to_code):
    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

def translate_en_to_es_nmt(src_sentence):
    print(f"openNMT")

    from_code = "en"
    to_code = "es"

    download_and_install_package(from_code, to_code)

    # Translate
    # translatedText = argostranslate.translate.translate("Hello World", from_code, to_code)
    translatedText = argostranslate.translate.translate(src_sentence, from_code, to_code)
    # print(translatedText)
    return translatedText

def translate_to_spanish(src, dest, target_language_code):
    # target language chosen is Spanish -> espionel - > code : "es"
    if (not pathlib.Path(src).exists() 
        or not pathlib.Path(dest).exists()):
        raise ValueError("video or destination folder do not exist")
    
    files = glob.glob(src + "/*.json")
    if not files:
        raise ValueError("No JSON files found in given directory")
    
    for file in files:
        # captions = {}
        
        with open(file) as f:
            captions = json.load(f)
        # print(caption["text"])

        print(f"translating {os.path.basename(file)}...", end="")
        # text = " Not since Watergate has an attorney general been at the center of such a firestorm."
        translator = Translator(to_lang=target_language_code)

        # translation = translator.translate(caption["text"])
        # caption['text'] = translation
        # print(f"{ caption['text']} in spanish: {translation}")
        for caption in captions["segments"]:
            # Split the input text into chunks with a maximum length of 500 characters
            # chunk_size = 500
            # translation = ""
            # for i in range(0, len(caption['text']), chunk_size):
            #     chunk = caption['text'][i:i + chunk_size]
            #     chunk_translation = translator.translate(chunk)
            #     translation += chunk_translation
            # caption['text'] = translator.translate(caption["text"]) this worked
            caption['text'] = translate_en_to_es_nmt(caption["text"])

        dest_file = os.path.join(dest, os.path.basename(file))
        print(f"saving result to {dest_file}")
        with open(dest_file, "w", encoding="utf-8") as file:
            file.write(json.dumps(captions) + "\n")


# def translate_to_spanish_dict(src, dest, target_language_code):
#     dict = MultiDictionary () 
  
#     # to translate into German 
#     translation = dict.translate('en', "happy", to=target_language_code) 
#     print(translation) 
#     # return translation


# def create_en_to_es_dictionary():
#     test_keys = ["Rash", "Kil", "Varsha"]
#     test_values = [1, 4, 5]
 
#     # Printing original keys-value lists
#     print ("Original key list is : " + str(test_keys))
#     print ("Original value list is : " + str(test_values))
    
    
#     # create a list of tuples using enumerate()
#     tuples = [(key, value)
#             for i, (key, value) in enumerate(zip(test_keys, test_values))]
    
#     # convert list of tuples to dictionary using dict()
#     res = dict(tuples)
    
#     print ("Resultant dictionary is : " + str(res))

if __name__ == '__main__':
    src_en_folder = "./transcriptions_en"
    destination_es_folder = "./transcriptions_es"
    pathlib.Path(destination_es_folder).mkdir(parents=True, exist_ok=True)
    # translate_to_spanish(src_en_folder, destination_es_folder, "es")
    translate_en_to_es_nmt()

    # translate_to_spanish_dict(src_en_folder, destination_es_folder, "es")