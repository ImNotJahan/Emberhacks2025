from latex_extension.data import MeasuredData

def send_llm_parsing(equation: str, variables: dict[str, MeasuredData | float]) -> tuple[str, str, str]:
    """
    Takes in a python equation (as a string) and a dictionary full of variables, and then evaluates the expression
    using those variables. Returns a tuple, with the first element being the result (value and uncertainty); the second
    the step-by-step calculation of the expression, formatted as an HTML table; and the third being two equations
    for the value and for the uncertainty, which culminate all the calculations of the expression into single equations.
    """

    result = eval(equation, variables)
    table_wrapper  = "<table>{}</table>"
    header_wrapper = "<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>"
    row_wrapper    = "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>"
    step_by_step   = header_wrapper.format("Value step", "Step result", "Uncertainty step", "Step uncertainty")

    md_s = lambda x: str(x).split("±")

    for value_step, uncertainty_step, data_point in zip(*result.all_steps_sequential()):
        step_by_step += row_wrapper.format(
            value_step,
            md_s(data_point)[0],
            uncertainty_step,
            md_s(data_point)[1]
        )

    step_by_step = table_wrapper.format(step_by_step)

    return str(result), step_by_step, "Long form equations (eventually)"