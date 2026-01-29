from profound2001.core.pattern import Pattern, PatternConstraints
from profound2001.runtime.context import Context

class Dangerous(Pattern):
    @property
    def constraints(self) -> PatternConstraints:
        return PatternConstraints(
            time_complexity="Unknown", 
            provenance="Assimilated",
            negative_capabilities=[]
        )

    def execute(self, ctx: Context) -> None:
        import os
        os.system('echo dangerous')
