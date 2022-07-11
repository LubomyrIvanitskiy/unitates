
# Unitates

It is a simple yet powerful package for creating and working with units of measurement.
You can simply create your own units or use predefined ones.

Supports all mathematical operations,
construction of complex units such as m/s, kg/m^2, etc., unit conversions,
comparison of units, basic work with arrays.

Feel free to ask questions, suggest new ideas, open new issues and create pull requests. 

I will be happy to cooperate!

## Usage

### Using predefined units
```python
from units.constants.time import *
from units.constants.length import *

>>> km(2) # create a unit with constructor
2 km
>>> 2*km # create a unit by multiplication
2 km
>>> 2>>km # create a unit by conversion operator (overloaded rshift)
2 km
>>> 2*km + 3*m # result will be always in lower units
2003 m
>>> 2*m/sec
2 m/sec
>>> 3*m / sec(2)
1.5 m/sec
>>> 2*m/sec >> km/hr # unit conversion
7.2 km/hr
>>> a=[[1,2,3], [4,5,6]] >> m/sec**2 # list conversion
>>> a
[[1 m/sec^2, 2 m/sec^2, 3 m/sec^2], [4 m/sec^2, 5 m/sec^2, 6 m/sec^2]]
>>> a >> km/hr**2
[[12960 km/hr^2, 25920 km/hr^2, 38880 km/hr^2], [51840 km/hr^2, 64800 km/hr^2, 77760 km/hr^2]]
>>> 10*m/sec**2 > 2*km/hr**2 # comparasion example 
True
>>> 60*min == 1*hr # equality
True
>>> d = {60*sec: "a"} #hash overriding
>>> min in d
True
```

### Creating your own units
```python
>>> from units import create_units
>>> characters, words, sentences, paragraphs, pages, chapters, books = create_units("Book", characters=1, words=4.7, sentences=21, paragraphs=3.5, pages=3, chapters=13, books=3)
>>> hound_of_the_baskervilles_book = 256*pages
>>> hound_of_the_baskervilles_book >> words
56447.99999999999 words
```




