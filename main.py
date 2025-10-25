import json
from latex_extension.data import MeasuredData

def main():
    """
    Initialize server and everything
    """
    pass

def parce_json(json_text):
    data = json.loads(json_text)["variables"]
    equation = json.loads(json_text)["equation"]["python_string_repr"]
    newdata = {}
    for dic in data:
        newdata[dic["name"]] = MeasuredData(dic["value"],dic["uncertainty"])
    
    return newdata, equation

if __name__ == "__main__":
    main()