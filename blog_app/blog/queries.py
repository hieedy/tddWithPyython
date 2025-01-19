import uuid

from blog_app.blog.models import Article
from pydantic import BaseModel
from typing import List


class ListArticleQuery(BaseModel):

    # Despite having no parameters here, for consistency we inherited from BaseModel.
    def execute(self) -> List[Article]:
        articles = Article.list()
        return articles


class GetArticleByIDQuery(BaseModel):

    id: str

    def execute(self) -> Article:
        article = Article.get_by_id(self.id)
        return article



