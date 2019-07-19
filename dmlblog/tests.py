import pytest

from .models import Post

pytestmark = pytest.mark.django_db


class TestPostModel:
    def test_save(self) -> None:
        product = Post.objects.create(
            author="Test Post author", title="Test Post title", text="Test Post text"
        )
        assert product.name == "Test Post author"
        assert product.title == "Test Post title"
        assert product.text == "Test Post text"
        assert isinstance(product.name, str)
