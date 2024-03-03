
from typing import Any, Dict, Optional

from app.api.models.models import TokenBlocklist, User


class SericeHelper():

    @staticmethod
    def create_post_res(posts: Any) -> Dict[str, Any]:
        """
        Create a dictionary representation of a post and its associated comments.

        Args:
            posts (object): A Post object containing information about the post.

        Returns:
            dict: A dictionary containing information about the post and its comments.
        """ # noqa
        res = {}
        if posts:
            res["post_id"] = posts.post_id
            res["post_content"] = posts.post_content
            res["post_likes"] = posts.likes
            res["post_by"] = posts.user.username
            res["created_date"] = posts.created_date.strftime("%Y-%m-%d %H:%M:%S") # noqa
            res["post_comments"] = [
                {
                    "comment_id": item.comment_id,
                    "comment": item.comment,
                    "comment_by": item.user.username,
                    "comment_date": item.comment_date.strftime("%Y-%m-%d %H:%M:%S") # noqa

                } for item in posts.postcomments]

        return res

    @staticmethod
    def is_user_exists(username: str) -> Optional[User]:
        """
        Check if a user with the given username exists.

        Args:
            username (str): The username to check.

        Returns:
            Optional[User]: The user object if it exists, else None.
        """# noqa
        return User.query.filter_by(username=username).first()

    @staticmethod
    def token_in_block_list(jti: str) -> Optional[TokenBlocklist]:
        """
        Check if a JWT token is in the blocklist.

        Args:
            jti (str): The JTI (JWT ID) to check.

        Returns:
            Optional[TokenBlocklist]: The TokenBlocklist object if the token is in the blocklist, else None.
        """ # noqa
        return TokenBlocklist.query.filter_by(jti=jti).first()
