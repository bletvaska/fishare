from pydantic import ValidationError
import pytest
from fishare.models.file import File

pytestmark = [pytest.mark.models, pytest.mark.file]


def test_when_no_data_are_provided_then_exception_raises():
    with pytest.raises(ValidationError):
        File()


def test_when_only_filename_is_provided_then_exception_raises(faker):
    with pytest.raises(ValidationError):
        File(filename=faker.file_name())


def test_when_only_size_is_provided_then_raise_exception(faker):
    with pytest.raises(ValidationError):
        File(size=faker.random_int(1000, 1000000))


def test_when_empty_filename_and_size_are_provided_then_raise_exception(faker):
    with pytest.raises(ValidationError):
        File(filename="", size=faker.random_int(1000, 1000000))


# def test_when_filename_is_empty_then_raise_exception():
#     with pytest.raises(ValidationError):
#         File(filename="")
