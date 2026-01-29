from profound2001.core.pattern import Pattern, PatternConstraints
from profound2001.runtime.context import Context

class Add(Pattern):
    """Adds 'a' and 'b' from context."""
    @property
    def constraints(self) -> PatternConstraints:
        return PatternConstraints(time_complexity="O(1)", provenance="System Canon")

    def execute(self, ctx: Context) -> None:
        a = ctx.get("a", 0)
        b = ctx.get("b", 0)
        ctx.set("result", a + b)
        print(f"Add: {a} + {b} = {a+b}")

class Sub(Pattern):
    """Subtracts 'b' from 'a'."""
    @property
    def constraints(self) -> PatternConstraints:
         return PatternConstraints(time_complexity="O(1)", provenance="System Canon")

    def execute(self, ctx: Context) -> None:
        a = ctx.get("a", 0)
        b = ctx.get("b", 0)
        ctx.set("result", a - b)
        print(f"Sub: {a} - {b} = {a-b}")
