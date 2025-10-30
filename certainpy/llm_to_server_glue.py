import json
from .latex_extension.data import MeasuredData

def parse_json(json_text: str) -> tuple[dict[str, MeasuredData | float], str]:
    """
    This function takes in the JSON response of the LLM, containing the equation and variables provided by the
    user, and then parses them into a state more usable for computation.
    """
    parsed_json = json.loads(json_text)

    json_dict = parsed_json["variables"]
    equation = parsed_json["equation"]["python_string_repr"]

    parsed_dict = {}
    for variable in json_dict:
        # if the uncertainty is zero, we just treat it as a float
        # otherwise, turn it into a MeasuredData object
        if variable["uncertainty"] == 0:
            parsed_dict[variable["name"]] = float(variable["value"])
        else:
            parsed_dict[variable["name"]] = MeasuredData(variable["value"], variable["uncertainty"])

    return parsed_dict, equation