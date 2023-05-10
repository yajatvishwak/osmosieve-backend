from dotenv import load_dotenv
import openai
import re
import os
import pandas as pd
import datetime
load_dotenv()
openai.api_key = os.getenv("OPENAI")
model_engine = "text-davinci-003"


def transform(path, command, applyTransformation=True):
    data = pd.read_csv(path)
    print("Model : ", model_engine)
    print("CSV Path : ", path)
    print("Detected Columns : ")
    print("\t\n".join([str(stuffs) for stuffs in list(data.columns)]))
    print("Recieved Command: ")
    print("\t"+command)
    print("Generated Prompt: ")

    prompt = "assume a dataframe called 'data' with columns " + ",".join([str(stuffs) for stuffs in list(
        data.columns)]) + ". "+"generate code that " + command + " in pandas 2.0 python 3.7; dont generate example, do not use external libraries"
    print("\t" + prompt)
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    generatedCode = completion.choices[0].text.strip()
    print("Generated Transformation Code: ")
    print("\t" + generatedCode)
    if applyTransformation:
        print("Data before transformation:")
        print(data)
        oldData = data.copy()
        op = exec(generatedCode)
        print("Data after transformation:")
        print(data)
        return {"oldTableValues": oldData.to_dict(orient="records"), "oldColumns": list(oldData.columns), "columns": list(data.columns), "tableValues": data.to_dict(orient="records"), "generatedCode": generatedCode}
