from unittest import TestCase
from enum import Enum

from pyerrors.pyerrors import Errors

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
        with self.assertRaises(AssertionError) as context:
            e.add_event(1)
        self.assertTrue(Errors.err_msg in str(context.exception))

    def test_check_accumulation(self):
        e = EventSummary(enum_class=MyEnum)
        for _ in range(10):
            e.add_event(MyEnum.member_a)
        for _ in range(20):
            e.add_event(MyEnum.member_b)
        self.assertEquals(e.get_event_count(MyEnum.member_a), 10)
        self.assertEquals(e.get_event_count(MyEnum.member_b), 20)
        self.assertEquals(e.get_event_count(MyEnum.member_c), 0)

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
        self.assertEquals(e1.get_event_count(MyEnum.member_a), 30)
        self.assertEquals(e1.get_event_count(MyEnum.member_b), 30)
        self.assertEquals(e1.get_event_count(MyEnum.member_c), 0)

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
