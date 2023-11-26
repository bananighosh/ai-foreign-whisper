import pathlib
import torch
from TTS.api import TTS
import json
import glob

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS with the target model name
tts = TTS(model_name="tts_models/es/mai/tacotron2-DDC", progress_bar=False).to(device)

def text_from_file(file_path) -> str:
    with open(file_path, 'r') as file:
        trans = json.load(file)
    return trans["text"]

def files_from_dir(dir_path) -> list:
    SUFFIX = ".json"
    pth = pathlib.Path(dir_path)
    if not pth.exists():
        raise ValueError("provided path does not exist")

    es_files = glob.glob(str(pth) + "/*.json")

    if not es_files:
        raise ValueError(f"no {SUFFIX} files found in {pth}")

    return es_files

def text_to_speech(text, output_file_path):
    # Run TTS
    tts.tts_to_file(text=text, file_path=str(output_file_path))

def text_file_to_speech(source_path):
    "reads source_path and output wav file to OUTPUT_PATH/<source_path_file_name>.wav"
    save_name = pathlib.Path(source_path).stem + ".wav"
    print(f"generating {save_name}...", end="")
    save_path = pathlib.Path(OUTPUT_PATH) / pathlib.Path(save_name)
    text = text_from_file(source_path)
    text_to_speech(text, str(save_path))
    print("success!")
    return None


if __name__ == '__main__':
    SOURCE_PATH = "./transcriptions_es"
    OUTPUT_PATH = "./audios/"

    # create output path if does not exist
    pathlib.Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
    
    files = files_from_dir(SOURCE_PATH)
    for file in files:
        text_file_to_speech(file)
