import enum
from collections import defaultdict
from typing import DefaultDict
from typing import Iterable, Union

"""
The errors class must be pickle ready since we may use it in multi-process, multi-thread or concurrent.futures
contexts in which every thread or process will report it's errors using this class.

A result of this is that we cannot hold the traceback object as is is not pickle able:
TypeError: can't pickle traceback objects
This means that if we want to store tracebacks as example we must convert them into some
string format that can be pickled.
"""


class EventSummary:
    err_msg = "only enum values are allowed"

    def __init__(
            self,
            enum_class: enum.Enum.__class__=None,
            enum_classes: Iterable[enum.Enum.__class__]=None,
            num_exceptions_saved: int=5,
    ) -> None:
        if enum_class is not None:
            self.enum_classes = [enum_class]  # type: Iterable[Iterable]
        if enum_classes is not None:
            self.enum_classes = enum_classes  # type: Iterable[Iterable]
        self.events = defaultdict(int)  # type: DefaultDict[int]
        self.num_exceptions_saved = num_exceptions_saved  # type: int
        self.exceptions_count = defaultdict(int)
        self.exceptions_saved = defaultdict(list)

    def add_event(self, value) -> None:
        assert any(isinstance(value, cls) for cls in self.enum_classes), EventSummary.err_msg
        self.events[value] += 1

    def get_event_count(self, value) -> int:
        assert any(isinstance(value, cls) for cls in self.enum_classes), EventSummary.err_msg
        return self.events[value]

    def get_enum_classes(self) -> Iterable[Iterable]:
        return self.enum_classes

    def add(self, event_summary: 'EventSummary') -> None:
        for cls in self.enum_classes:  # type: Iterable
            for enum_member in cls:
                self.events[enum_member] += event_summary.events[enum_member]

    def add_many(self, event_summaries: Iterable['EventSummary']) -> None:
        for event_summary in event_summaries:
            self.add(event_summary)

    def print(self, title=None) -> None:
        if title:
            print(title)
        for cls in self.enum_classes:  # type: Iterable
            for enum_member in cls:
                print("event {} happened {} times".format(enum_member.name, self.events[enum_member]))
        for exception_type, exception_count in self.exceptions_count.items():
            print("exception_type {} happened {} time(s)".format(exception_type, exception_count))

    def __enter__(self):
        pass

    def __exit__(self, e_type, e_val, trace_back) -> Union[bool, None]:
        if e_type is not None:
            self.exceptions_count[e_type] += 1
            if len(self.exceptions_saved[e_type]) < self.num_exceptions_saved:
                self.exceptions_saved[e_type].append((e_val, "trace_back"))
            return True
