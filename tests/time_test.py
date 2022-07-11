import math
import pytest

from units import Units
from units.constants.time import *
from units.constants.length import *


def test_time_creation_by_singletone_multiplication():
    a = 1.2 * hr
    assert type(a) == Units
    assert a.value == 1.2
    assert a.units == {"hr": 1}


def test_time_addition():
    assert 1.5 * hr + 30 * min == 120 * min
    assert 1.5 * hr + 30 * min == 2 * hr


def test_number_addition():
    assert 1 * hr + 2 == 3 * hr
    assert 1 * min + 2 == 3 * min


def test_time_substraction():
    assert 2 * min - 5 * sec == 115 * sec


def test_number_substraction():
    assert 3.5 * hr - 1 == 2.5 * hr


def test_multiplication_by_number():
    assert 2 * day * 1.2 == 2.4 * day


def test_multiplication_by_time():
    assert (2 * day) * (12 * hr) == 576 * hr  # cause 2 day * 0.5 day = 1 day


def test_division_by_time():
    assert 2 * day / (2 * day) == 1


def test_division_by_number():
    assert 2 * day / 2 == 24 * hr


def test_casting_representation():
    assert str(2 * hr) == "2 hr"
    assert str(sec(2 * hr)) == "7200 sec"


def test_different_units_equality():
    assert 2 * min == 120 * sec == 120000 * ms
    assert day == 24 * hr
    assert week - day == 6 * day


def test_correct_power():
    assert 1 / sec == sec(1) ** -1
    assert sec(2) ** 2 != 2 * sec ** 2
    assert math.sqrt(sec ** 2) == sec
    assert min ** 5 / min ** 2 == min ** 3
    with pytest.raises((AttributeError, AssertionError, ValueError)):
        sec ** sec
    with pytest.raises((AttributeError, AssertionError, ValueError)):
        3 ** sec


def test_comparison_and_hashes():
    assert min(1) > sec(3)
    assert min(1) > sec(3)
    assert hash(day) == hash(24 * hr)
    d = dict()
    d[60 * hr] = "a"
    d[60 * min] = "b"
    d[1 * hr] = "c"
    assert "a" in d.values()
    assert "c" in d.values()
    assert "b" not in d.values()  # b is overridden by c, because 60 * min and 1 * hr have same hashes


# """
# MULTIGROUP
# """
def test_different_groups():
    # print(convert_unit(m/sec, km/hr))
    # print(m >> km)
    print(m / sec + m / sec)