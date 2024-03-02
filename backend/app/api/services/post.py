from app.api.models.models import Posts
from app.utils.common_utils import SericeHelper

servicehelper = SericeHelper()


# This class handle the creation of post
class PostCreator():
    def __init__(self, data) -> None:
        self.data = data

    def process_data(self):
        _RESPONSE = []
        try:
            post_content = self.data.get("post_content")
            new_post = Posts.create_post(post_content, 1)
            _RESPONSE.append(
                {
                    'post_id': new_post.post_id,
                    'post_content': new_post.post_content,
                    'likes': new_post.likes
                }
            )
            return {"data": _RESPONSE}

        except Exception as e:
            raise e


# This class handle getting the post
class PostGetter():
    def __init__(self) -> None:
        pass

    def process_all_posts(self):
        try:
            # Get all the posts
            all_posts = [
                servicehelper.create_post_res(x) for x in Posts.query.all()]
            return {"data": all_posts}

        except Exception as e:
            raise e
