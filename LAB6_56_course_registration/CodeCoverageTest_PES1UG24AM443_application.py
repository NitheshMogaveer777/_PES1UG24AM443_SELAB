
import pytest

from course_registration import (
    can_register,
    waitlist_position,
    late_fee
)


# Test 1: Can register function
def test_can_register_all_statements():

    with pytest.raises(ValueError, match="unknown status"):
        can_register("visitor", 0, 3, True)

    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, 0, True)

    assert can_register("regular", 0, 3, False) == "prerequisites missing"

    assert can_register("regular", 23, 2, True) == "credit limit exceeded"

    assert can_register("regular", 20, 4, True) == "registered"


# Test 2: Waitlist function
def test_waitlist_all_statements():

    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)

    assert waitlist_position(5, 10, 0) == 0

    assert waitlist_position(10, 10, 10) == -1

    assert waitlist_position(10, 10, 2) == 3


# Test 3: Late fee function
def test_late_fee_all_statements():

    assert late_fee(0, 10, False) == 0

    assert late_fee(5, 10, True) == 0

    assert late_fee(5, 25, False) == 750

    assert late_fee(10, 25, False) == 1050

    assert late_fee(30, 25, False) == 2000
