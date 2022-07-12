from collections import OrderedDict, namedtuple
from numbers import Number
from typing import List, Union, Iterable

from units.constants import PREDEFINED_GROUP_LIST


def align_arguments(func):
    def wrapper(*args):
        new_args = _align_units(*args)
        return func(*new_args)

    return wrapper


class Units(float):

    def __new__(cls, value: float, units: dict):
        assert type(value) == int or type(value) == float, \
            f"Your are trying to create unit from {type(value)}. Maybe some brackets are missed?"
        return float.__new__(cls, value)

    def __init__(self, value: float, units: dict):
        self.value: float = value
        self.units: dict = units

    def __str__(self):
        v = self.value if self.value % 1 > 0 else int(self.value)
        split_units = [[], []]
        for u in self.units:
            if self.units[u] > 0:
                split_units[0].append(u)
            elif self.units[u] < 0:
                split_units[1].append(u)

        def _unit_string(unit, power):
            if power > 1:
                return f"{unit}^{power}"
            elif power == 1:
                return f"{unit}"
            elif power == 0:
                return ""

        lines = [
            "*".join([_unit_string(u, self.units[u]) for u in split_units[0]]),
            "*".join([_unit_string(u, -self.units[u]) for u in split_units[1]])
        ]
        if not len(lines[0]) and len(lines[1]):
            lines[0] = "1"
        for i, line in enumerate(lines):
            if len(split_units[i]) > 1:
                lines[i] = "(" + line + ")"
        return f"{v} {lines[0]}{'/' if len(lines[1]) else ''}{lines[1]}"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def _add_vectors(vector_1, vector_2):
        new_vector = [v1 + v2 for v1, v2 in zip(vector_1, vector_2)]
        return _vecto_to_units(new_vector)

    @staticmethod
    def _are_vectors_same(vector_1, vector_2):
        return all([v1 == v2 for v1, v2 in zip(vector_1, vector_2)])

    @align_arguments
    def __mul__(self, other):
        return _create_units_object(float(self) * float(other),
                                    self._add_vectors(_units_to_vector(self), _units_to_vector(other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    @align_arguments
    def __truediv__(self, other):
        return _create_units_object(float(self) / float(other),
                                    self._add_vectors(_units_to_vector(self), _units_to_vector(other, inverse=True)))

    @align_arguments
    def __rtruediv__(self, other):
        return _create_units_object(float(other) / float(self),
                                    self._add_vectors(_units_to_vector(self, inverse=True), _units_to_vector(other)))

    @align_arguments
    def __floordiv__(self, other):
        return _create_units_object(float(self) // float(other),
                                    self._add_vectors(_units_to_vector(self), _units_to_vector(other, inverse=True)))

    @align_arguments
    def __rfloordiv__(self, other):
        return _create_units_object(float(other) // float(self),
                                    self._add_vectors(_units_to_vector(self, inverse=True), _units_to_vector(other)))

    @align_arguments
    def __add__(self, other):
        assert isinstance(other, Number) and not isinstance(other, Units) or self._are_vectors_same(
            _units_to_vector(self), _units_to_vector(other)), \
            "Cannot add values with different units"

        return _create_units_object(float(self) + float(other), self.units)

    @align_arguments
    def __radd__(self, other):
        return self.__add__(other)

    @align_arguments
    def __sub__(self, other):
        assert isinstance(other, Number) and not isinstance(other, Units) or self._are_vectors_same(
            _units_to_vector(self), _units_to_vector(other)), \
            "Cannot subtract values with different units"

        return _create_units_object(float(self) - float(other), self.units)

    @align_arguments
    def __rsub__(self, other):
        assert self._are_vectors_same(_units_to_vector(self), _units_to_vector(other)), \
            "Cannot subtract values with different units"

        return _create_units_object(float(other) - float(self), self.units)

    @align_arguments
    def __pow__(self, power, modulo=None):
        assert isinstance(power, Number) and not isinstance(power, Units), "Raising to the Units object makes no sense"
        return _create_units_object(float.__pow__(self, power, modulo), {u: power * p for u, p in self.units.items()})

    @align_arguments
    def __rpow__(self, power, modulo=None):
        raise AttributeError("Raising to the Units object makes no sense")

    def __rshift__(self, other):
        if isinstance(other, SingleUnits):
            return _convert_unit(self, other)
        else:
            raise "Incorrect argument for right-shift operator. Should be SingleUnit instance"

    @align_arguments
    def __eq__(self, other):
        return float(self) == float(other)

    @align_arguments
    def __le__(self, other):
        return float(self) <= float(other)

    @align_arguments
    def __lt__(self, other):
        return float(self) < float(other)

    @align_arguments
    def __ge__(self, other):
        return float(self) >= float(other)

    @align_arguments
    def __gt__(self, other):
        return float(self) > float(other)

    def __hash__(self):
        group_to_min_unit = _get_minimum_unit_by_group()
        converted_value = _convert_unit(self, [group_to_min_unit[unit_to_group[unit]] for unit in self.units])
        return hash(str(converted_value))


class SingleUnits(Units):

    def __new__(cls, units: dict):
        return super().__new__(cls, 1, units)

    def __init__(self, units: dict):
        self.units = units
        super().__init__(1, units)

    def __call__(self, value):
        if isinstance(value, Units):
            return _convert_unit(value, list(self.units.keys()))
        else:
            return _create_units_object(value, self.units)

    def __rrshift__(self, other):
        if isinstance(other, Units):
            return _convert_unit(other, self)
        elif isinstance(other, float) or isinstance(other, int):
            return _create_units_object(other, self.units)
        elif isinstance(other, Iterable):
            res = []
            for obj in other:
                res.append(self.__rrshift__(obj))
            return res
        else:
            raise "Incorrect argument for right-shift operator. Should be float or Units"


def _create_units_object(value: float, units: dict):
    if value == 1:
        return SingleUnits(units)
    else:
        return Units(value, units)


def __getattr__(name):
    if name not in globals():
        return "unit_to_object" in dir and unit_to_object[name]
    else:
        raise AttributeError


def _convert_unit(v: Units, to_units: Union[str, List[str], Units]):
    if isinstance(to_units, List):
        pass
    elif isinstance(to_units, str):
        assert len(v.units) == 1, "cannot convert multi-unit object to the single unit"
        to_units = [to_units]
    elif isinstance(to_units, SingleUnits):
        assert all([unit_to_group[u1] == unit_to_group[u2] for u1, u2 in zip(v.units, to_units.units)]), \
            "Cannot perform conversion between different unit groups"
        assert all([v.units[u1] == to_units.units[u2] for u1, u2 in zip(v.units, to_units.units)]), \
            "Cannot perform conversion between units raised to different power"
        to_units = list(to_units.units.keys())
    else:
        raise ValueError(f"Incorrect to_units type {type(to_units)}")

    assert len(v.units) == len(to_units), "to_units length should match the value units length"
    if all([u1 == u2 for u1, u2 in zip(v.units.keys(), to_units)]):
        return v

    from_units = list(v.units.keys())

    multipliers = []
    for i, (from_unit, to_unit) in enumerate(zip(from_units, to_units)):
        assert unit_to_group[from_unit] == unit_to_group[to_unit], \
            "Cannot perform conversion between units from different groups"
        assert v.units[from_unit]

        fraction = unit_to_weight[from_unit] / unit_to_weight[to_unit]
        multipliers.append(fraction)
    scaler = 1
    for multiplier, power in zip(multipliers, v.units.values()):
        scaler *= multiplier ** power
    return _create_units_object(v.value * scaler, {unit: power for unit, power in zip(to_units, v.units.values())})


def _units_to_vector(v: Union[Units, Number], inverse=False) -> List:
    unit_names = list(unit_to_weight.keys())
    vector = [0] * len(unit_names)
    if not isinstance(v, Units):
        return vector
    for i, unit in enumerate(unit_names):
        if unit in v.units:
            vector[i] = v.units[unit] if not inverse else -v.units[unit]
    return vector


def _vecto_to_units(vector) -> dict:
    unit_names = list(unit_to_weight.keys())
    res = {}
    for i, v in enumerate(vector):
        if v != 0:
            res[unit_names[i]] = v
    return res


def _align_units(*args):
    min_units_per_group = {}

    for a in args:
        if not isinstance(a, Units):
            continue
        for unit, power in a.units.items():
            group = unit_to_group[unit]
            if group not in min_units_per_group:
                min_units_per_group[group] = unit
            elif unit_to_weight[unit] < unit_to_weight[min_units_per_group[group]]:
                min_units_per_group[group] = unit

    new_args = []
    for a in args:
        if not isinstance(a, Units):
            new_args.append(a)
        else:
            to_units = []
            for unit in a.units:
                group = unit_to_group[unit]
                min_group_unit = min_units_per_group[group]
                to_units.append(min_group_unit)
            res = _convert_unit(a, to_units)
            new_args.append(res)
    return new_args


def _get_minimum_unit_by_group():
    min_units_per_group = {}
    for unit in unit_to_group:
        group = unit_to_group[unit]
        if group not in min_units_per_group:
            min_units_per_group[group] = unit
        elif unit_to_weight[unit] < unit_to_weight[min_units_per_group[group]]:
            min_units_per_group[group] = unit
    return min_units_per_group


####################
## Public API
####################

def create_units(group_name: str = "common", weight_type="rel", **unit_map):
    if "unit_to_weight" not in globals():
        global unit_to_weight
        unit_to_weight = OrderedDict()
    if "unit_to_group" not in globals():
        global unit_to_group
        unit_to_group = OrderedDict()
    if "unit_to_object" not in globals():
        global unit_to_object
        unit_to_object = OrderedDict()
    if "group_to_units" not in globals():
        global group_to_units
        group_to_units = OrderedDict()

    if weight_type == "rel":
        new_map = {}
        prev_value = 1
        for k, v in unit_map.items():
            prev_value = new_map[k] = v * prev_value
        unit_map = new_map

    res = []
    for unit_name, weight in unit_map.items():
        if group_name in group_to_units:
            group_to_units[group_name].append(unit_name)
        else:
            group_to_units[group_name] = [unit_name]
        unit_to_group[unit_name] = group_name
        unit_to_weight[unit_name] = weight
        obj = SingleUnits({unit_name: 1})
        unit_to_object[unit_name] = obj
        res.append(obj)
    return res


def load_units(*unit_names, group_name: str = None, except_group_names: Union[None, str, List[str]] = None):
    res = OrderedDict()

    if group_name is not None:
        if "group_to_units" in globals() and group_to_units is not None and group_name in group_to_units:
            res.update({unit: unit_to_object[unit] for unit in group_to_units[group_name]})
        else:
            return None
    if except_group_names is not None and isinstance(except_group_names, str):
        except_group_names = [except_group_names]
    if len(unit_names) == 0 and group_name is None:
        name_list = unit_to_object.keys()
    else:
        name_list = unit_names
    for name in name_list:
        if except_group_names is None or unit_to_group[name] not in except_group_names:
            res[name] = unit_to_object[name]
    if len(res) == 0:
        return None
    elif len(res) == 1:
        return next(iter(res.values()))
    else:
        UnitsPack = namedtuple("UnitsPack", " ".join(res.keys()))
        return UnitsPack(**res)


def destroy_units(group_name: str = None, except_group_names: Union[None, str, List[str]] = PREDEFINED_GROUP_LIST):
    if except_group_names is not None and isinstance(except_group_names, str):
        except_group_names = [except_group_names]
    if "unit_to_group" not in globals():
        return  # nothing to clear. No units yet
    if group_name is not None:
        if except_group_names is not None and group_name in except_group_names:
            raise AttributeError("Cannot destroy group from the except_group_names list")
        groups_names = [group_name]
    else:
        groups_names = list(set(unit_to_group.values()))
    for group_name in groups_names:
        if except_group_names is not None and group_name in except_group_names:
            continue
        if group_name in group_to_units:
            for name in group_to_units[group_name]:
                del unit_to_object[name]
                del unit_to_weight[name]
                del unit_to_group[name]
            del group_to_units[group_name]
