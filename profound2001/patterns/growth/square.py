from profound2001.core.pattern import Pattern
from profound2001.runtime.context import Context

class Square(Pattern):
    def execute(self, ctx: Context) -> None:
                
        x = ctx.get("x", 5)
        ctx.set("square", x * x)
        print(f"Square of {x} is {x*x}")
