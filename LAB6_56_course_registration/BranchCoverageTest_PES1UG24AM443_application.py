
import pytest

from course_registration import (
    can_register,
    waitlist_position,
    late_fee
)


# Test 1: Registration outcomes
@pytest.mark.parametrize(
    'status,current,course,prereq,expected',
    [
        ('regular', 20, 4, True, 'registered'),
        ('probation', 10, 3, True, 'registered'),
        ('honors', 25, 3, True, 'registered'),

        ('regular', 23, 2, True, 'credit limit exceeded'),
        ('probation', 16, 1, True, 'credit limit exceeded'),
        ('honors', 28, 1, True, 'credit limit exceeded'),

        ('regular', 0, 3, False, 'prerequisites missing'),
    ]
)
def test_can_register_outcomes(
    status, current, course, prereq, expected
):
    assert can_register(
        status, current, course, prereq
    ) == expected


# Test 2: Registration errors
@pytest.mark.parametrize(
    'status,course',
    [
        ('unknown', 3),
        ('regular', 0),
        ('regular', -2)
    ]
)
def test_can_register_errors(status, course):

    with pytest.raises(ValueError):
        can_register(status, 0, course, True)


# Test 3: Waitlist outcomes
@pytest.mark.parametrize(
    'enrolled,capacity,waitlist,expected',
    [
        (3, 5, 0, 0),
        (5, 5, 0, 1),
        (8, 5, 4, 5),
        (5, 5, 10, -1),
        (5, 5, 12, -1)
    ]
)
def test_waitlist_outcomes(
    enrolled, capacity, waitlist, expected
):
    assert waitlist_position(
        enrolled, capacity, waitlist
    ) == expected


# Test 4: Invalid capacity
def test_waitlist_invalid_capacity():

    with pytest.raises(ValueError, match='invalid capacity'):
        waitlist_position(0, 0, 0)


# Test 5: Late fee outcomes
@pytest.mark.parametrize(
    'days,credits,waiver,expected',
    [
        (0, 10, False, 0),
        (-2, 25, False, 0),
        (5, 10, True, 0),
        (5, 25, False, 750),
        (7, 10, False, 500),
        (8, 10, False, 600),
        (10, 25, False, 1050),
        (30, 10, False, 2000),
        (30, 25, False, 2000)
    ]
)
def test_late_fee_outcomes(
    days, credits, waiver, expected
):
    assert late_fee(
        days, credits, waiver
    ) == expected
