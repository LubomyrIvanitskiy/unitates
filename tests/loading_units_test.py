from units import create_units, load_units, destroy_units, SingleUnits, PREDEFINED_GROUP_LIST
import pytest


@pytest.fixture
def reset_all_units():
    destroy_units()


@pytest.fixture
def create_book_units():
    yield create_units(group_name="BookUnits", words=1, pages=500, books=200)
    # destroy_units("BookUnits")


@pytest.fixture
def create_mass_units():
    create_units(group_name="MassUnits", grams=1, kilograms=1000)
    # destroy_units("MassUnits")


@pytest.fixture
def init(reset_all_units, create_book_units, create_mass_units):
    pass


def test_loading_by_group_name(init):
    words, pages, books = load_units(group_name="BookUnits")
    assert isinstance(words, SingleUnits)
    assert isinstance(pages, SingleUnits)
    assert isinstance(books, SingleUnits)


def test_loading_by_single_unit_name(init):
    pages = load_units("pages")
    assert isinstance(pages, SingleUnits)
    assert pages.units == {"pages": 1}


def test_loading_by_multiple_unit_names(init):
    pages, books = load_units("pages", "books")
    assert isinstance(pages, SingleUnits)
    assert isinstance(books, SingleUnits)
    assert pages.units == {"pages": 1}
    assert books.units == {"books": 1}


def test_loading_units_pack(init):
    u = load_units("pages", "books")
    assert isinstance(u.pages, SingleUnits)
    assert isinstance(u.books, SingleUnits)
    assert u.pages.units == {"pages": 1}
    assert u.books.units == {"books": 1}


def test_loading_all(init):
    units = load_units(except_group_names=PREDEFINED_GROUP_LIST)
    assert all([str(a) == b for a, b in zip(units, ["1 words", "1 pages", "1 books", "1 grams", "1 kilograms"])])


def test_group_deletion(init):
    destroy_units("MassUnits")
    units = load_units(except_group_names=PREDEFINED_GROUP_LIST)
    assert all([str(a) == b for a, b in zip(units, ["1 words", "1 pages", "1 books"])])


def test_all_deletion(init):
    destroy_units(except_group_names=PREDEFINED_GROUP_LIST)
    units = load_units(except_group_names=PREDEFINED_GROUP_LIST)
    assert units is None
