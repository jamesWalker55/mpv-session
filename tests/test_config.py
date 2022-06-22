import lib.config as config
import os.path
import pytest
import tempfile


def read_file(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()


def describe_config():
    @pytest.fixture
    def c():
        with tempfile.TemporaryDirectory() as dirpath:
            path = os.path.join(dirpath, "config.txt")

            yield config.Config(path)

    def it_accepts_absolute_paths():
        with tempfile.TemporaryDirectory() as dirpath:
            path = os.path.join(dirpath, "config.txt")
            c = config.Config(path)

        assert c.get_config_path() == path

    def it_writes_an_empty_file_with_no_data(c):
        c.data = None
        c.save()

        assert read_file(c.get_config_path()) == ""

    def it_writes_a_simple_dictionary(c):
        c.data = {"a": 1, "b": 2}
        c.save()

        assert read_file(c.get_config_path()) == '{"a": 1, "b": 2}'

    def it_loads_none_if_the_file_does_not_exist(c):
        c.data = "hello"

        c.load()

        assert c.data == None

    def it_restores_data_correctly(c):
        data = {"a": 1, "b": 2}

        c.data = data.copy()
        c.save()
        c.load()

        assert c.data == data
