from contextlib import contextmanager
import tempfile
import pytest


@pytest.fixture
def temporary_file():
    @contextmanager
    def _temporary_file(content):
        file_obj = tempfile.NamedTemporaryFile(mode='w+')
        file_obj.write(content)
        file_obj.seek(0)
        yield file_obj
        file_obj.close()
    return _temporary_file
