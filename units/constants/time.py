from units import create_units
from units.constants import PREDEFINED_GROUP_LIST

ms, sec, min, hr, day, week = create_units(PREDEFINED_GROUP_LIST[1], ms=1, sec=1000, min=60, hr=60, day=24, week=7)
