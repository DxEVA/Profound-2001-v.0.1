from profound2001.core.pattern import Pattern, PatternConstraints
from profound2001.runtime.context import Context

class Huge_function(Pattern):
    @property
    def constraints(self) -> PatternConstraints:
        return PatternConstraints(
            time_complexity="Unknown", 
            provenance="Assimilated",
            negative_capabilities=[]
        )

    def execute(self, ctx: Context) -> None:
        def huge_function():
            print("Line 1")
            print("Line 2")
            print("Line 3")
            print("Line 4")
            print("Line 5")
            print("Line 6")
            print("Line 7")
            print("Line 8")
            print("Line 9")
            print("Line 10")
            print("Line 11")
            print("Line 12")
            print("Line 13")
            print("Line 14")
            print("Line 15")
            print("Line 16")
            print("Line 17")
            print("Line 18")
            print("Line 19")
            print("Line 20")
            print("Line 21")
            print("Line 22")
            print("Line 23")
            print("Line 24")
            print("Line 25")
            print("This function is too long!")
        result = huge_function()
        ctx.set('huge_function', result)
        print(f'huge_function: {result}')
