import json
from latex_extension.data import MeasuredData

def main():
    """
    Initialize server and everything
    """
    pass

def parce_json(json_text):
    data = json.loads(json_text)["variables"]
    newdata = {}
    for dic in data:
        newdata[dic["name"]] = MeasuredData(dic["value"],dic["uncertainty"])
    return newdata

if __name__ == "__main__":
    main()