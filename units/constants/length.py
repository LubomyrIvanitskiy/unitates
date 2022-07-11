from units import create_units
from units.constants import PREDEFINED_GROUP_LIST

mm, cm, m, km = create_units(PREDEFINED_GROUP_LIST[0], mm=1, cm=10, m=100, km=1000)