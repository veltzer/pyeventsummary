""" pyeventsummary.py """

from enum import Enum
from collections import defaultdict
from collections.abc import Iterable
from typing import DefaultDict, Type
import sys


class EventSummary:
    """
    The errors class must be pickle ready since we may use it in multi-process, multi-thread or concurrent.futures
    contexts in which every thread or process will report its errors using this class.

    A result of this is that we cannot hold the traceback object as is is not pickle able:
    TypeError: cant pickle traceback objects
    This means that if we want to store tracebacks as example we must convert them into some
    string format that can be pickled.
    """

    err_msg = "only enum values are allowed"

    def __init__(
            self,
            # We specify that the class must be a *subclass* of Enum, not just any type.
            enum_class: Type[Enum] | None = None,
            enum_classes: list[Type[Enum]] | None = None,
            num_exceptions_saved: int = 10,
            num_events_data_saved: int = 10,
    ) -> None:
        classes: list[Type[Enum]] = []
        if enum_class is not None:
            classes = [enum_class]
        if enum_classes is not None:
            classes = enum_classes
        # This more specific type hint is the key to the fix.
        self.enum_classes: list[Type[Enum]] = classes
        self.events: DefaultDict[Enum, int] = defaultdict(int)
        self.num_exceptions_saved: int = num_exceptions_saved
        self.num_events_data_saved: int = num_events_data_saved
        self.events_data_saved: DefaultDict[Enum, list] = defaultdict(list)
        self.exceptions_count: DefaultDict[type, int] = defaultdict(int)
        self.exceptions_saved: DefaultDict[type, list] = defaultdict(list)

    def add_event(self, value: Enum, data=None) -> None:
        assert any(isinstance(value, cls) for cls in self.enum_classes), EventSummary.err_msg
        self.events[value] += 1
        if data is not None and len(self.events_data_saved[value]) < self.num_events_data_saved:
            self.events_data_saved[value].append(data)

    def get_event_count(self, value: Enum) -> int:
        assert any(isinstance(value, cls) for cls in self.enum_classes), EventSummary.err_msg
        return self.events[value]

    def get_enum_classes(self) -> Iterable[Type[Enum]]:
        return self.enum_classes

    def add(self, event_summary: "EventSummary") -> None:
        for cls in self.enum_classes:
            # mypy now knows "cls" is an Enum class and is iterable.
            for enum_member in cls:
                self.events[enum_member] += event_summary.events[enum_member]
                self.events_data_saved[enum_member].extend(event_summary.events_data_saved[enum_member])

    def add_many(self, event_summaries: Iterable["EventSummary"]) -> None:
        for event_summary in event_summaries:
            self.add(event_summary)

    def print(self, title: str | None = None, output_file_handle=sys.stdout, show_zero_events: bool = False) -> None:
        if title:
            print(title, file=output_file_handle)
        print("counts", file=output_file_handle)
        for cls in self.enum_classes:
            for enum_member in cls:
                num_events = self.events[enum_member]
                if num_events > 0 or show_zero_events:
                    print(f"event {enum_member.name} happened {num_events} times",
                          file=output_file_handle)
        print("exceptions", file=output_file_handle)
        for exception_type, exception_count in self.exceptions_count.items():
            print(f"exception_type {exception_type} happened {exception_count} time(s)",
                  file=output_file_handle)
        print("event types", file=output_file_handle)
        for event_type, event_data_list in self.events_data_saved.items():
            print(f"event type {event_type}", file=output_file_handle)
            for event_data in event_data_list:
                print(f"\tdata [{event_data}]", file=output_file_handle)

    def __enter__(self):
        pass

    def __exit__(self, e_type, e_val, trace_back) -> bool | None:
        if e_type is not None:
            self.exceptions_count[e_type] += 1
            if len(self.exceptions_saved[e_type]) < self.num_exceptions_saved:
                self.exceptions_saved[e_type].append((e_val, "trace_back"))
            return True
        return None
