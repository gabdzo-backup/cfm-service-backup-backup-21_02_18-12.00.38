"""Step model."""

from dataclasses import dataclass


@dataclass
class Step:
    """Model to represent step."""

    do: str

    @staticmethod
    def from_dict(do):
        """From dict."""
        return Step(do)


@dataclass
class TimeStep(Step):
    """Model to represent time step."""

    time: int
    unit: str

    @staticmethod
    def from_dict(do, time, unit):
        """From dict."""
        return TimeStep(do, time, unit)


@dataclass
class ToolStep(Step):
    """Model to represent tool step."""

    tool: str

    @staticmethod
    def from_dict(do, tool):
        """From dict."""
        return ToolStep(do, tool)


@dataclass
class UntilStep(Step):
    """Model to represent until step."""

    until: str

    @staticmethod
    def from_dict(do, until):
        """From dict."""
        return UntilStep(do, until)


type_map = {
    "step": Step,
    "time_step": TimeStep,
    "tool_step": ToolStep,
    "until_step": UntilStep,
}


def from_dict(step_dict):
    """From dict."""
    assert len(step_dict) == 1
    for k, v in step_dict.items():
        return type_map[k].from_dict(**v)
