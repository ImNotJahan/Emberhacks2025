# certainPY
*Be certain with your uncertainty!*

certainPY is a library/webapp for evaluating equations utilizing measured data points. It produces answers with 
automatic error propagation, and allows for the generation of its evaluation's steps as ready-to-use LaTeX
equations.

The library for doing these calculations and LaTeX productions is found under [/latex_extension](latex_extension),
which expands upon the MeasuredData class of the [PhysicsTools](https://github.com/ImNotJahan/PhysicsTools) library to
allow for all of this extra functionality. But worry not-- no knowledge of Python nor of how to use this library is
needed to reap its benefits! Using Google Gemini, we have created a frontend which can parse any arbitrarily-provided
equation and variables, producing valid code which is evaluated and clearly displayed, all through the webapp frontend.

All the code for interfacing with Gemini is located in [/llm_interface](llm_interface), with the rules for parsing in
the [json_arsing_rules.txt](llm_interface/json_parsing_rules.txt) file. Gemini parses the expression provided to create
a JSON file containing a classical Python equation and a list of variables. By ensuring Gemini only handles technologies
it knows well, we reduce the risk of incorrect parsings to almost zero. Once the parsing is done, the evaluation is
done fully in good-old handwritten code, ensuring that all calculations are as correct as any calculator could get them.
Thus, one can worry free have the convenience of AI, paired with the reliability of predefined computation.

Connecting the two is our Flask application and glue scripts, found in the root directory of this repository, along with
parts in the [static/](static) and [templates/](templates) directories.