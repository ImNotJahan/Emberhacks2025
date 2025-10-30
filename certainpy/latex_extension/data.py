from physics_tools.data import MeasuredData as md

class VariableLabel:
    def __init__(self, label: str):
        self.label = label

    def __str__(self):
        return self.label

var_letters = ['x', 'y', 'z', 'w', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
self_mapping_var_letters = {x: x for x in var_letters}
self_mapping_var_letters.update({"s_" + x: "s_" + x for x in var_letters})

class MeasuredData(md):
    """
    The (latex-extended) MeasuredData class creates a data point which automatically propagates uncertainty with
    every calculation done with, and keeps a log of every value and uncertainty calculation, allowing for generation
    of LaTeX equations demonstrating the evaluation of the object's state.
    """
    def __init__(self, measurement: float, error: float,
                 value_step=None, uncertainty_step=None, step_variables=None,
                 value_wrapped=False, uncertainty_wrapped=False):
        super().__init__(measurement, error)

        self.value_step          = value_step
        self.uncertainty_step    = uncertainty_step
        self.has_steps           = value_step and uncertainty_step
        self.step_variables      = step_variables
        # these are for deciding if parentheses should put around these equations when forming composites
        self.value_wrapped       = value_wrapped
        self.uncertainty_wrapped = uncertainty_wrapped

    # for the most part, just overriding methods on the physics_tools MeasuredData to add LaTeX templates

    def __add__(self, other):
        return MeasuredData(
            (result := super().__add__(other)).value,
            result.error(),
            r"@x@+@y@",
            r"\sqrt{@s_x@^2+@s_y@^2}" if isinstance(other, MeasuredData) else r"@s_x@",
            [self, other],
            True,
            False
        )

    def __radd__(self, other):
        return MeasuredData(
            (result := super().__radd__(other)).value,
            result.error(),
            r"@y@+@x@",
            r"\sqrt{@s_y@^2+@s_x@^2}" if isinstance(other, MeasuredData) else r"@s_x@",
            [self, other],
            True,
            False
        )

    def __sub__(self, other):
        return MeasuredData(
            (result := super().__sub__(other)).value,
            result.error(),
            r"@x@-@y@",
            r"\sqrt{@s_x@^2+@s_y@^2}"  if isinstance(other, MeasuredData) else r"@s_x@",
            [self, other],
            False,
            False
        )

    def __mul__(self, other):
        return MeasuredData(
            (result := super().__mul__(other)).value,
            result.error(),
            r"@x@\cdot@y@",
            r"@x@\cdot@y@\sqrt{\frac{@s_x@}{@x@}^2+\frac{@s_y@}{@y@}^2}" if isinstance(other, MeasuredData) else
            r"@s_x@\cdot@y@",
            [self, other],
            False,
            True
        )

    def __rmul__(self, other):
        return MeasuredData(
            (result := super().__rmul__(other)).value,
            result.error(),
            r"@y@\cdot@x@",
            r"@x@\cdot@y@\sqrt{\frac{@s_y@}{@y@}^2+\frac{@s_x@}{@x@}^2}" if isinstance(other, MeasuredData) else
            r"@s_x@\cdot@y@",
            [self, other],
            False,
            True
        )

    def __truediv__(self, other):
        return MeasuredData(
            (result := super().__truediv__(other)).value,
            result.error(),
            r"\frac{@x@}{@y@}",
            r"@x@\cdot@y@\sqrt{\frac{@s_x@}{@x@}^2+\frac{@s_y@}{@y@}^2}" if isinstance(other, MeasuredData) else
            r"\frac{@s_x@}{@y@}",
            [self, other],
            True,
            True
        )

    def __pow__(self, other: int):
        return MeasuredData(
            (result := super().__pow__(other)).value, # abs(other * self.value ** (other - 1) * s)
            result.error(),
            r"@x@^{@y@}",
            r"\left|@y@\cdot@s_x@\cdot@x@^{@y@ - 1}\right|",
            [self, other],
            False,
            False

        )

    def sine(self):
        return MeasuredData(
            (result := super().sine()).value,  # abs(s * math.cos(self.value))
            result.error(),
            r"\sin @x@",
            r"\left|@s_x@ \cos @x@\right|",
            [self],
            False,
            False
        )

    def cosine(self):
        return MeasuredData(
            (result := super().cosine()).value,
            result.error(),
            r"\cos @x@",
            r"\left|@s_x@ \sin @x@\right|",
            [self],
            False,
            False
        )

    def tangent(self):
        return MeasuredData(
            (result := super().tangent()).value,
            result.error(),
            r"\tan @x@",
            r"\left|@s_x@ \sec @x@^2\right|",
            [self],
            False,
            False
        )

    def arctan(self):
        # s / (1 + self.value ** 2)
        return MeasuredData(
            (result := super().arctan()).value,
            result.error(),
            r"\arctan @x@",
            r"\frac{@s_x@}{1+@x@^2}",
            [self],
            False,
            False
        )

    def arcsin(self):
        # s / math.sqrt(1 - self.value ** 2)
        return MeasuredData(
            (result := super().arcsin()).value,
            result.error(),
            r"\arcsin @x@",
            r"\frac{@s_x@}{\sqrt{1-@x@^2}}",
            [self],
            False,
            False
        )

    def __neg__(self):
        return MeasuredData(
            (result := super().__neg__()).value,
            result.error(),
            r"-@x@",
            r"@s_x@",
            [self],
            False,
            False
        )

    def __abs__(self):
        return MeasuredData(
            (result := super().__abs__()).value,
            result.error(),
            r"\left|@x@\right|",
            r"@s_x@",
            [self],
            False,
            False
        )

    # from here on out, we have some latex_extension unique methods for MeasuredData

    def recent_step(self, value_step, plug_in_vars=True, trunc_nums=True) -> str:
        if value_step:
            step = self.value_step
        else:
            step = self.uncertainty_step

        if plug_in_vars:
            md_p = lambda x: isinstance(x, MeasuredData) # measured data predicate (i.e., is measured data)
            md_s = lambda x: str(x).split("±") # measured data split
            en_v = lambda: enumerate(self.step_variables) # enumerate (step) variables

            if trunc_nums:
                norm_vars = {var_letters[i]: md_s(v)[0] for i, v in en_v() if md_p(v)}
                norm_vars.update({var_letters[i]: v for i, v in en_v() if not md_p(v)})
                err_vars  = {"s_" + var_letters[i]: md_s(v)[1] for i, v in en_v() if md_p(v)}
            else:
                norm_vars = {var_letters[i]: v.value for i, v in en_v() if md_p(v)}
                norm_vars.update({var_letters[i]: v for i, v in en_v() if not md_p(v)})
                err_vars = {"s_" + var_letters[i]: v.error() for i, v in en_v() if md_p(v)}

            vals = norm_vars
            vals.update(err_vars)
        else:
            vals = self_mapping_var_letters
        return at_format(step, vals)

    def all_steps_sequential(self, plug_in_vars=True, trunc_nums=True) -> tuple[list[str], list[str], list]:
        value_steps       = []
        uncertainty_steps = []
        data_points       = []

        # recursively add steps of any previously calculated MeasuredDatas to step lists
        def apnd_step(dp: MeasuredData):
            value_steps.append(dp.recent_step(True, plug_in_vars, trunc_nums))
            uncertainty_steps.append(dp.recent_step(False, plug_in_vars, trunc_nums))

            data_points.append(dp)

            for sdp in dp.step_variables:
                if isinstance(sdp, MeasuredData) and sdp.has_steps:
                    apnd_step(sdp)

        apnd_step(self)

        # reverse step lists so that earliest steps are first
        return value_steps[::-1], uncertainty_steps[::-1], data_points

    def all_steps_composite(self, plug_in_vars=True, trunc_nums=True) -> tuple[str, str]:
        seen_variables = {}

        def expand_eqs(dp: MeasuredData) -> tuple[object, object]:
            nonlocal seen_variables

            md_p = lambda x: isinstance(x, MeasuredData)  # measured data predicate (i.e., is measured data)
            md_s = lambda x: str(x).split("±")  # measured data split
            en_v = lambda: enumerate(dp.step_variables)  # enumerate (step) variables

            if not dp.has_steps:
                if plug_in_vars:
                    if trunc_nums:
                        val, err = md_s(dp)
                        return float(val), float(err)
                    else:
                        return dp.value, dp.error()
                else:
                    if dp not in seen_variables:
                        seen_variables[dp] = var_letters[len(seen_variables)]

                    return (VariableLabel(" {} ".format(seen_variables[dp])),
                            VariableLabel(" s_{} ".format(seen_variables[dp])))

            norm_vars = {var_letters[i]: expand_eqs(v)[0] for i, v in en_v() if md_p(v)}
            norm_vars.update({var_letters[i]: v for i, v in en_v() if not md_p(v)})
            err_vars = {"s_" + var_letters[i]: expand_eqs(v)[1] for i, v in en_v() if md_p(v)}

            vals = norm_vars
            vals.update(err_vars)

            return (at_format(dp.value_step, vals, dp.value_wrapped),
                    at_format(dp.uncertainty_step, vals, dp.uncertainty_wrapped))

        value_eq, error_eq = expand_eqs(self)
        return value_eq, error_eq

def at_format(s: str, vals: dict[str, MeasuredData | float | str], abhor_parentheses=False):
    """
    Formats a string, replacing variables wrapped in @'s with values from a dict

    Needed, since the built-in formatting methods do not play well with LaTeX (would either require an obscene number
    of backslashes, or don't work with certain important characters.)

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

        # being a string indicates it's a compound equation
        # (or could be a compound equation). Thus, we wrap
        # in parentheses for safety
        if isinstance(val, str) and not abhor_parentheses: formatted += r"\left("

        # for measured datas, make sure outputting in latex rep
        if isinstance(val, MeasuredData) or isinstance(val, md):
            formatted += val.latex().replace("$", "")
        else:
            formatted += str(val)

        if isinstance(val, str) and not abhor_parentheses: formatted += r"\right)"

        s = s[x+1:]

    return formatted + s

if __name__ == "__main__":
    import doctest
    doctest.testmod()