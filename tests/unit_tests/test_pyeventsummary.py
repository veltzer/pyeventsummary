""" test_pyeventsummary.py """

from enum import Enum
from typing import Any
from unittest import TestCase

import pytest

from pyeventsummary.pyeventsummary import EventSummary


class MyEnum(Enum):
    member_a = 1
    member_b = 2
    member_c = 3


class TestErrors(TestCase):
    def test_create(self):
        _ = EventSummary(enum_class=MyEnum)

    def test_create_and_pass_one_good(self):
        e = EventSummary(enum_class=MyEnum)
        e.add_event(MyEnum.member_a)

    def test_create_and_pass_one_bad(self):
        e = EventSummary(enum_class=MyEnum)
        not_an_enum: Any = 1
        with pytest.raises(AssertionError) as context:
            e.add_event(not_an_enum)
        assert EventSummary.err_msg in str(context.value)

    def test_check_accumulation(self):
        e = EventSummary(enum_class=MyEnum)
        for _ in range(10):
            e.add_event(MyEnum.member_a)
        for _ in range(20):
            e.add_event(MyEnum.member_b)
        assert e.get_event_count(MyEnum.member_a) == 10
        assert e.get_event_count(MyEnum.member_b) == 20
        assert e.get_event_count(MyEnum.member_c) == 0

    def test_aggregation(self):
        e1 = EventSummary(enum_class=MyEnum)
        e2 = EventSummary(enum_class=MyEnum)
        for _ in range(10):
            e1.add_event(MyEnum.member_a)
            e2.add_event(MyEnum.member_b)
        for _ in range(20):
            e1.add_event(MyEnum.member_b)
            e2.add_event(MyEnum.member_a)
        e1.add(e2)
        assert e1.get_event_count(MyEnum.member_a) == 30
        assert e1.get_event_count(MyEnum.member_b) == 30
        assert e1.get_event_count(MyEnum.member_c) == 0

    def test_print(self):
        e = EventSummary(MyEnum)
        for _ in range(10):
            e.add_event(MyEnum.member_a)
        for _ in range(20):
            e.add_event(MyEnum.member_b)
        e.print()

    def test_catch_exception(self):
        e = EventSummary(MyEnum)
        with e:
            raise ValueError("this is an exception")
        e.print()
