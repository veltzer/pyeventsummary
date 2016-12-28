import enum
from collections import defaultdict
from typing import Iterable


"""
The errors class must be pickleble since we may use it in multi-process, multi-thread or concurrent.futures
contexts in which every thread or process will report it's errors using this class.

A result of this is that we cannot hold the traceback object as is as it is not picklable:
TypeError: can't pickle traceback objects
This means that if we want to store tracebacks as example we must convert them into some
string format that can be pickled.
"""


class EventSummary:
    err_msg = "only enum values are allowed"

    def __init__(
            self,
            enum_class: enum.Enum.__class__=None,
            enum_classes: list[enum.Enum.__class__]=None,
            num_exceptions_saved: int=5,
    ):  # type -> None
        if enum_class is not None:
            self.enum_classes = [enum_class]  # type: list[Iterable]
        if enum_classes is not None:
            self.enum_classes = enum_classes
        self.events = defaultdict(int)
        self.num_exceptions_saved = num_exceptions_saved
        self.exceptions_count = defaultdict(int)
        self.exceptions_saved = defaultdict(list)

    def add_event(self, value):  # type -> None
        assert any(isinstance(value, cls for cls in self.enum_classes))
        self.events[value] += 1

    def get_event_count(self, value):  # type -> int
        assert any(isinstance(value, cls for cls in self.enum_classes))
        return self.event[value]

    def get_enum_classes(self):  # type -> list[class]
        return self.enum_classes

    def add(self, errors: 'Errors'):  # type -> None
        for cls in self.enum_classes:
            for enum_member in cls:
                self.events[enum_member] += errors.events[enum_member]

    def print(self, title=None):  # type -> None
        if title:
            print(title)
        for enum_member in self.enum_class:
            print("event {} happened {} times".format(enum_member.name, self.errors[enum_member]))
        for exception_type, exception_count in self.exceptions_count.items():
            print("exception_type {} happened {} time(s)".format(exception_type, exception_count))

    def __enter__(self):
        pass

    def __exit__(self, e_type, e_val, trace_back):  # type -> Union[bool, None]
        if e_type is not None:
            self.exceptions_count[e_type] += 1
            if len(self.exceptions_saved[e_type]) < self.num_exceptions_saved:
                self.exceptions_saved[e_type].append((e_val, "trace_back"))
            return True
