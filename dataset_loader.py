import re
import os

import json

def load_dataset():
    with open("alignments/manifest_with_output_file_paths.json", "r") as f:
        results = []
        
        data = f.read().split("\n")[:-1]
        for line in data:
            matches = re.findall(r'(?:[\s\S]*?\"audio_filepath\"\:\s\"([\S\s]*?)\"\,\s\"text\"\:\s\"([\s\S]*?)\")', line)
            
            new_file = {
                "audio_filepath": matches[0][0],
                "text": matches[0][1],
                "tokens": [],
                "durations": []
            }
            
            results.append(new_file)
            # print("==================\n", matches)

            
        token_path = "alignments/ctm/tokens/"
        files = os.listdir(token_path)
        
        for file in files:
            with open(f"{token_path}/{file}", "r") as token_file:
                tokens = token_file.read().split("\n")[:-1]
                afile = results[[i for i in range(len(results)) if file[:-3] in results[i]["audio_filepath"]][0]]
                
                
                
                for line in tokens:
                    filename, _, start, duration, token, _, _, _ = line.split(" ")
                    afile["tokens"].append(token)
                    afile["durations"].append((start, duration))

                
        return results

def load_manifest():
    with open("recordings/manifest.json", "r") as data:
        result = json.load(data)

    return result

def save_dataset():
    ds = load_dataset()
   
            
    out_file = "recordings/manifest.json"
   
    with open(out_file, "w") as f:
        json.dump(ds, f, indent=4)
        

