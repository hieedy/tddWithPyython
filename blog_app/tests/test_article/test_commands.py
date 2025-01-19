import pytest
from blog_app.blog.models import Article
from blog_app.blog.commands import CreateArticleCommand, AlreadyExists

def test_create_article():
    """
    GIVEN CreateArticleCommand with valid author, title, and content
    WHEN the execute method is called
    THEN a new article must exist in the database with the same attributes.
    """
    cmd = CreateArticleCommand(
        author='john@doe.com',
        title='New Article',
        content='Super awesome article'
    )
    article = cmd.execute()
    db_article = Article.get_by_id(article.id)

    assert db_article.id == article.id
    assert db_article.author == article.author
    assert db_article.title == article.title
    assert db_article.content == article.content


def test_create_article_already_exists():
    """
    GIVEN CreateArticleCommand with the data that has same title which already exists in the db.
    WHEN the execute method is called
    THEN the AlreadyExists exception must be raised
    """
    Article(
        author='john@doe.com',
        title='New Article',
        content='Super awesome article'
    ).save()

    cmd = CreateArticleCommand(
        author='john@doe.com',
        title='New Article',
        content='Super awesome article'
    )

    with pytest.raises(AlreadyExists):
        cmd.execute()

# Test cover the following use cases
# article should be created for valid data.
# article title must be unique.
