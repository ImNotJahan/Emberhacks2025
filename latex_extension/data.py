from physics_tools.data import MeasuredData as md

class MeasuredData(md):
    def __init__(self, measurement: float, error: float, steps=None):
        super().__init__(measurement, error)
        # (eq, (variables..))
        self.steps = steps if steps else [] # contains LaTeX of eq used for each step of uncertainty calculations, & values used

    def error(self):
        return super().error()

    def __add__(self, other):
        new_steps = self.steps.copy()
        new_steps.append((
            r"\sqrt{@s_x@^2+@s_y@^2}",
            (self, other)
        ))
        result = super().__add__(other)
        return MeasuredData(result.value, result.error(), steps=new_steps)

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

    def __str__(self) -> str:
        return super().__str__()

    def uncertainty_equations(self, max_depth: int) -> list[tuple[str, tuple]]:
        pass

    def get_steps(self):
        return self.steps

def at_format(s: str, vals: dict[str, MeasuredData]):
    formatted = ""

    print(s, vals)

    while x := s.find("@") != -1:
        formatted += s[:x]
        print(s, formatted)
        s = s[x+1:]
        x = s.find("@")

        print(s)

        if x == -1:
            raise ValueError("Expected another @ symbol!")

        formatted += str(vals[s[:x]])
        s = s[x+1:]

        print(s, formatted)

    return formatted