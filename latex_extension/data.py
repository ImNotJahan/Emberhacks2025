from physics_tools.data import MeasuredData as md

var_letters = ['x', 'y', 'z', 'w']
self_mapping_var_letters = {x: x for x in var_letters}
self_mapping_var_letters.update({"s_" + x: "s_" + x for x in var_letters})

class MeasuredData(md):
    """
    The (latex-extended) MeasuredData class creates a data point which automatically propagates uncertainty with
    every calculation done with, and keeps a log of each uncertainty calculation, allowing those calculations to be
    formatted in LaTeX. Ok and for normal calculations, it seems we need. TODO rewrite this description better
    """
    def __init__(self, measurement: float, error: float, value_step=None, uncertainty_step=None, step_variables=None):
        super().__init__(measurement, error)

        self.value_step       = value_step
        self.uncertainty_step = uncertainty_step
        self.has_steps        = value_step and uncertainty_step
        self.step_variables   = step_variables

    # for the most part, just overriding methods on the physics_tools MeasuredData to add more functionality

    def __add__(self, other):
        value_step = r"@x@+@y@"
        uncertainty_step = r"\sqrt{@s_x@)^2+@s_y@^2}"
        step_variables = [self, other]

        result = super().__add__(other)
        return MeasuredData(result.value, result.error(), value_step, uncertainty_step, step_variables)

    def __radd__(self, other):
        return super().__radd__(other)

    def __sub__(self, other):
        return super().__sub__(other)

    def __mul__(self, other):
        return super().__mul__(other)

    def __rmul__(self, other):
        return super().__rmul__(other)

    def __truediv__(self, other):
        return super().__truediv__(other)

    def __pow__(self, other: int):
        return super().__pow__(other)

    def sine(self):
        return super().sine()

    def cosine(self):
        return super().cosine()

    def tangent(self):
        return super().tangent()

    def arctan(self):
        return super().arctan()

    def arcsin(self):
        return super().arcsin()

    def __neg__(self):
        return super().__neg__()

    def __abs__(self):
        return super().__abs__()

    # from here on out, we have some latex_extension unique methods for MeasuredData

    def uncertainty_equations(self, max_depth: int) -> list[tuple[str, tuple]]:
        pass

    def recent_step(self, value_step, plug_in_vars=True, trunc_nums=True) -> str:
        if value_step:
            step = self.value_step
        else:
            step = self.uncertainty_step

        if plug_in_vars:
            if trunc_nums:
                norm_vars = {var_letters[i]: str(v).split("±")[0] for i, v in enumerate(self.step_variables)}
                err_vars  = {"s_" + var_letters[i]: str(v).split("±")[1] for i, v in enumerate(self.step_variables)}
            else:
                norm_vars = {var_letters[i]: v.value for i, v in enumerate(self.step_variables)}
                err_vars = {"s_" + var_letters[i]: v.error() for i, v in enumerate(self.step_variables)}
            vals = norm_vars
            vals.update(err_vars)
        else:
            vals = self_mapping_var_letters
        return at_format(step, vals, True)

    def all_steps_sequential(self, plug_in_vars=True, trunc_nums=True) -> tuple[list[str], list[str]]:
        value_steps       = []
        uncertainty_steps = []

        # recursively add steps of any previously calculated MeasuredDatas to step lists
        def apnd_step(dp: MeasuredData):
            value_steps.append(dp.recent_step(True, plug_in_vars, trunc_nums))
            uncertainty_steps.append(dp.recent_step(False, plug_in_vars, trunc_nums))

            for sdp in dp.step_variables:
                if isinstance(sdp, MeasuredData) and sdp.has_steps:
                    apnd_step(sdp)

        apnd_step(self)

        # reverse step lists so that earliest steps are first
        return value_steps[::-1], uncertainty_steps[::-1]

def at_format(s: str, vals: dict[str, MeasuredData | float], add_parenthesis=False):
    """
    Formats a string, replacing variables wrapped in @'s with values from a dict

    >>> at_format("@hi@", {"hi": 7})
    '7'
    >>> at_format("The value is @x@", {"x": MeasuredData(0.77, 0.5)})
    'The value is 0.8 \\\\pm 0.5'
    """
    assert s.count("@") & 1 == 0

    formatted = ""

    while (x := s.find("@")) != -1:
        formatted += s[:x]

        s = s[x+1:]
        x = s.find("@")

        if x == -1:
            raise ValueError("Expected another @ symbol!")
        if (v := s[:x]) not in vals:
            raise ValueError(v + " is not in vals")

        val = vals[v]

        if add_parenthesis: formatted += r"\left("

        # for measured datas, make sure outputting in latex rep
        if isinstance(val, MeasuredData) or isinstance(val, md):
            formatted += val.latex().replace("$", "")
        else:
            formatted += str(val)

        if add_parenthesis: formatted += r"\right)"

        s = s[x+1:]

    return formatted + s

if __name__ == "__main__":
    import doctest
    doctest.testmod()