import os

from typing import Any
import logging

try:
    from google import genai
    from google.genai.types import GenerateContentResponse as GCR
except ImportError:
    # Create placeholders in case of fail
    class GCR:
        """Mock placeholder for GenerateContentResponse."""

        def __init__(self, text=""):
            self.text = text


    class genai:
        class Client:
            def __init__(self):
                pass

            class models:
                def generate_content(self, model: str, contents: str):
                    # Should be mocked in unit tests
                    raise NotImplementedError(
                        "Gemini Client not available or mocked.")

class RequestsManager:
    __log = logging.getLogger("RequestsManager")

    def __init__(self, *, api_key: str=None):
        # Reads variables from the file
        info: tuple[str, str] = RequestsManager.read_vars()
        # Sets api key
        os.environ["GEMINI_API_KEY"] = info[0] if api_key is None else api_key
        # Applies rule set for parsing user's prompt
        self.rule_set = info[1]

    @staticmethod
    def read_vars() -> IOError | tuple[str, str]:
        """Reads api_key and json_parsing_rules from the files to use later
        """
        assert os.path.exists("api.txt"), "api_key exists"
        assert os.path.exists("json_parsing_rules.txt"), "rules file exists"

        RequestsManager.__log.critical("Reading files...")
        key, rules = None, None
        with open("api.txt", "r") as f:
            key = f.readline().split("=")[1]
        with open("json_parsing_rules.txt", "r") as f:
            rules = "".join(f.readlines())
        if key is None or rules is None:
            raise IOError("Failed reading variables")
        RequestsManager.__log.critical("Reading is finished.")
        return key, rules

    @staticmethod
    def __format_log(x: Any, y: str | GCR) -> str | TypeError:
        """Logging function for debugging"""
        if isinstance(y, str):
            return f"input: {x}\noutput: {y}\n"
        elif isinstance(y, GCR): # Use isinstance() instead of type() is Python best practice
            return f"input: {x}\noutput: {y.text}\n"
        raise TypeError("Incorrect type")

    @staticmethod
    def __process_json(json_string: str) -> str:
        """Strips response from Gemini removing unnecessary
        characters and converting the string into readable json"""
        return json_string.strip("```").lstrip("json")

    def __generate_answer(self, input_prompt: str) -> str:
        """Function that sends reqeust to Gemini AI

        :param input_prompt: prompt for LLM
        :return: LLM response
        """
        self.__log.critical("Sending the request...")
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=input_prompt
        )
        self.__log.critical(RequestsManager.__format_log(input_prompt, response))
        return response.text

    def __validate_prompt(self, input_prompt: str) -> AssertionError | bool:
        """Function validates if enough information was to preform calculations
        """
        validation_prompt = (input_prompt +
                             "\nAre there enough information to evaluate"
                             " the formula?"
                             " Answer yes or no without explanation please")
        response = self.__generate_answer(validation_prompt).lower()
        if "yes" in response and "no" in response:
            raise AssertionError("The answer is not clearly defined")
        elif "yes" in response: return True
        elif "no" in response: return False
        raise AssertionError("Response is invalid")

    def get_response(self, input_prompt: str) -> ValueError | str:
        """Given the prompt returns a json with equation and variables"""
        try:
            is_valid = self.__validate_prompt(input_prompt)
            self.__log.critical(f"is_valid={is_valid}")
            if not is_valid:
                raise ValueError("There are not enough information provided")
        except AssertionError:
            raise "Prompt has flaws"
        final_prompt = (input_prompt +
                        "\n" +
                        self.rule_set)
        response = self.__generate_answer(final_prompt)
        self.__generate_answer("Thank you for your help!")
        return self.__process_json(response)