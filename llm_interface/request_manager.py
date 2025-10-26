import os
from os import path

from typing import Any
import logging

import llm_to_server_glue

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
        api_file_path = path.join("llm_interface", "api.txt")
        rule_file_path = path.join("llm_interface", "json_parsing_rules.txt")

        assert os.path.exists(api_file_path), "api_key exists"
        assert os.path.exists(rule_file_path), "rules file exists"

        RequestsManager.__log.critical("Reading files...")
        key, rules = None, None
        with open(api_file_path, "r") as f:
            key = f.readline().split("=")[1]
        with open(rule_file_path, "r") as f:
            rules = "".join(f.readlines())
        if key is None or rules is None:
            raise IOError("Failed reading variables")
        RequestsManager.__log.critical("Reading is finished.")
        return key, rules

    @staticmethod
    def __format_log(x: Any, y: str | GCR) -> str | TypeError:
        """Logging function for debugging"""
        if isinstance(y, str):
            return f"req: {x}\noutput: {y}\n"
        elif isinstance(y, GCR): # Use isinstance() instead of type() is Python best practice
            return f"req: {x}\noutput: {y.text}\n"
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
        self.__log.critical("Sending the req...")
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=input_prompt
        )
        self.__log.critical(RequestsManager.__format_log(input_prompt, response))
        return response.text

    def __validate_prompt(self, input_prompt: str) -> str | bool:
        """Function validates if enough information was to preform calculations
        """
        validation_prompt = (input_prompt + """ 
        Is there enough information to evaluate the given formula by plugging in the provided variables? If there is,
        respond YES. Otherwise, respond with an explanation as to why, which the user can read and easily understand.""")

        response = self.__generate_answer(validation_prompt)

        if "YES" in response:
            return True

        return response


    def get_response(self, input_prompt: str) -> str:
        """Given the prompt returns a json with equation and variables"""
        try:
            is_valid = self.__validate_prompt(input_prompt)
            self.__log.critical(f"is_valid={is_valid}")

            if is_valid != True:
                return "[ERR]" + is_valid
        except AssertionError:
            raise "Prompt has flaws"
        final_prompt = (input_prompt +
                        "\n" +
                        self.rule_set)
        response = self.__generate_answer(final_prompt)

        return self.__process_json(response)