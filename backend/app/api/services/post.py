from typing import Any, Callable, Dict, List

from app.api.models.models import Posts, db
from app.utils.common_utils import SericeHelper

servicehelper = SericeHelper()


# This class handle the creation of post
class PostCreator():
    def __init__(self, data: Dict[str, Any],
                 user_identity: Callable[[], str]) -> None:
        """
        Initialize the PostCreator object with post data and user identity.

        Args:
            data (dict): A dictionary containing post data with the key "post_content".
            user_identity (callable): A function that returns the user's identity.
        """ # noqa
        self.post_content = data.get("post_content")
        self.user_id = user_identity()

    def process_data(self) -> Dict[str, Any]:
        """
        Process post data and create a new post.

        Returns:
            dict: A dictionary containing information about the newly created post.
        """ # noqa
        _RESPONSE = []
        try:

            new_post = Posts.create_post(self.post_content, self.user_id)
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
    def process_all_posts(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Process all posts and return them.

        Returns:
            dict: A dictionary containing a list of all posts.
        """
        try:
            # Get all the posts
            all_posts = [
                servicehelper.create_post_res(x) for x in Posts.query.all()]
            return {"data": all_posts}

        except Exception as e:
            raise e


class PostUpdate():
    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the PostUpdate object with post data.

        Args:
            data (dict): A dictionary containing post data with keys "post_id" and "post_content".
        """ # noqa
        self.post_id = data.get("post_id")
        self.post_content = data.get("post_content")

    def post_update(self) -> Dict[str, Any]:
        """
        Update an existing post.

        Returns:
            dict: A dictionary containing information about the updated post.
        """ # noqa
        _RESPONSE = {"data": []}
        try:
            older_post = Posts.query.get(self.post_id)
            older_post.post_content = self.post_content
            db.session.commit()
            _RESPONSE["data"].append({
                "post_id": self.post_id,
                "post_content": self.post_content
            })
            return _RESPONSE
        except Exception as e:
            raise e
