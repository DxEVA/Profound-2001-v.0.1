from profound2001.core.pattern import Pattern, PatternConstraints
from profound2001.runtime.context import Context

class HelloWorld(Pattern):
    @property
    def constraints(self) -> PatternConstraints:
        return PatternConstraints(
            time_complexity="O(1)",
            memory_estimate="Low",
            negative_capabilities=["No Network", "No IO"],
            provenance="System Canon"
        )
    def execute(self, context: Context) -> None:
        """
        Sets a greeting in the context.
        """
        user = context.get("user", "World")
        message = f"Hello, {user}!"
        context.set("greeting", message)
        print(message)
