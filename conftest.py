import pytest
import random
from dale.data.tokens import Token, TOKEN_TYPES


@pytest.fixture
def random_token():
    token_type = random.choice(TOKEN_TYPES)
    return token_type()