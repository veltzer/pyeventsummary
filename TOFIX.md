# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pyeventsummary/pyeventsummary.py:95` - `__exit__` saves the literal string `"trace_back"` instead of the traceback, so every saved exception loses its stack; the class docstring (lines 14-17) says the traceback must be converted to a picklable string - store `"".join(traceback.format_tb(trace_back))`.

## Medium

- `src/pyeventsummary/pyeventsummary.py:96` - `__exit__` returns `True` for every exception type, so `with summary:` also swallows `KeyboardInterrupt`, `SystemExit` and `GeneratorExit`; only suppress `Exception` subclasses (`issubclass(e_type, Exception)`).
- `src/pyeventsummary/pyeventsummary.py:88` - `__enter__` returns `None`, so `with EventSummary(...) as s:` binds `s` to `None`; return `self`.
- `src/pyeventsummary/pyeventsummary.py:57` - `add()` merges `events` and `events_data_saved` but drops `exceptions_count` and `exceptions_saved`, so aggregating per-process summaries (the use case in the class docstring) loses all exception counts; also `extend` at line 62 ignores the `num_events_data_saved` cap. Merge the exception dicts and respect the caps.
- `src/pyeventsummary/pyeventsummary.py:45` - argument validation is done with `assert`, which disappears under `python -O`, letting non-enum values be counted silently; raise `TypeError`/`ValueError` instead (and update `tests/unit_tests/test_pyeventsummary.py:25`).

## Low

- `src/pyeventsummary/pyeventsummary.py:31` - when both `enum_class` and `enum_classes` are passed, `enum_class` is silently discarded; combine them or raise.
- `src/pyeventsummary/pyeventsummary.py:68` - `print()` never outputs `exceptions_saved`, so the saved exception values/tracebacks are unreachable from the report; print them under the "exceptions" section.
- `tests/unit_tests/test_pyeventsummary.py:61` - `test_catch_exception` (and `test_print` at line 53) assert nothing; check `exceptions_count[ValueError] == 1` and the printed output.
