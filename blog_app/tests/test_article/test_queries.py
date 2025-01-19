from blog_app.blog.models import Article
from blog_app.blog.queries import ListArticleQuery, GetArticleByIDQuery


def test_list_articles():
    """
    GIVEN 2 articles stored in the database
    WHEN then execute method is invoked
    THEN it should return 2 articles.
    """
    Article(
        author='Jane@doe.com',
        title='New Aticle',
        content='Super extra awesom article'
    ).save()

    Article(
        author='jane@doe.com',
        title='Another Article',
        content='Super awesome article'
    ).save()
    query = ListArticleQuery()
    assert len(query.execute()) == 2

def test_get_article_by_id():
    """
    GIVEN ID of the article stored in the DB.
    WHEN execute method is called with the given ID
    THEN it should return the article with the same ID
    """
    article = Article(
        author='jane@doe.com',
        title='New Article',
        content='Super extra aswesom article'
    ).save()

    query = GetArticleByIDQuery(
        id=article.id
    )
    assert query.execute().id == article.id
