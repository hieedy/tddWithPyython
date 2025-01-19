# Will be used for storing pytest fixtures.
import os
import tempfile
import time

import pytest

from blog_app.blog.models import Article


# autouse set to True so that it's automatically used by default before and after
# each test in test suite. as we are using db everywhere so it's better to use this.

@pytest.fixture(autouse=True)
def database():
    _, file_name = tempfile.mkstemp()
    print(file_name)
    os.environ['DATABASE_NAME'] = file_name
    Article.create_table(database_name=file_name)
    yield
    retries = 5
    while retries > 0:
        try:
            os.unlink(file_name) #remove the file from the system
            break
        except PermissionError:
            retries -= 1
            time.sleep(0.1)
    else:
        print('Faied to delete the file.')

