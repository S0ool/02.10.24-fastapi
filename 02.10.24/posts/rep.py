from posts.models import Post
from repository.repository import BaseRepository


class PostRepository(BaseRepository):
    model = Post