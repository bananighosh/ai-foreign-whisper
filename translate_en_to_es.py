import pathlib
import glob
import json
import os

from pprint import pprint
from translate import Translator
# from PyDictionary import PyDictionary 
from PyMultiDictionary import MultiDictionary

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
            caption['text'] = translator.translate(caption["text"])

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
    translate_to_spanish(src_en_folder, destination_es_folder, "es")
    # translate_to_spanish_dict(src_en_folder, destination_es_folder, "es")