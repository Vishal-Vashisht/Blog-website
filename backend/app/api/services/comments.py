from app.api.models.models import Comments, db
from typing import Dict, Any, Callable


class CommentCreate():
    def __init__(self, data: Dict[str, Any],
                 user_identity: Callable[[], str]) -> None:
        """
        Initialize the CommentCreate object with comment data and user identity.

        Args:
            data (dict): A dictionary containing comment data with keys "comment" and "post_id".
            user_identity (callable): A function that returns the user's identity.
        """# noqa
        self.comment = data.get("comment")
        self.post_id = data.get("post_id")
        self.user_id = user_identity()

    def process_comment(self) -> Dict[str, Any]:
        """
        Process and create a new comment.

        Returns:
            dict: A dictionary containing information about the newly created comment.
        """ # noqa
        _RESPONSE = {"data": []}
        try:
            new_comment = Comments.create_comment(
                post_id=self.post_id,
                user=self.user_id,
                comment=self.comment
            )
            _RESPONSE["data"].append({
                "comment_id":  new_comment.comment_id,
                "comment": new_comment.comment,
                "post_id": new_comment.post_id,
                "comment_date": new_comment.comment_date.strftime("%Y-%m-%d %H:%M:%S") # noqa
            })
            return _RESPONSE
        except Exception as e:
            raise e


class CommentUpdate():

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the CommentUpdate object with comment data.

        Args:
            data (dict): A dictionary containing comment data with keys "comment_id" and "comment".
        """ # noqa
        self.comment_id = data.get("comment_id")
        self.comment = data.get("comment")

    def update_comment(self) -> Dict[str, Any]:
        """
        Update an existing comment.

        Returns:
            dict: A dictionary containing information about the updated comment.
        """ # noqa

        _RESPONSE = {"data": []}

        try:
            old_comment = Comments.query.get(self.comment_id)

            # Update the old comment to new comment
            old_comment.comment = self.comment
            db.session.commit()

            # Preapre the response
            _RESPONSE["data"].append({
                "comment_id": self.comment_id,
                "comment": self.comment
            })
            return _RESPONSE
        except Exception as e:
            raise e


class CommentDelete():

    def __init__(self, data: Dict[str, int]) -> None:
        """
        Initialize the CommentDelete object with comment data.

        Args:
            data (dict): A dictionary containing comment data with the key "comment_id".
        """ # noqa

        self.comment_id = data.get("comment_id")

    def delete_comment(self) -> Dict[str, Any]:
        """
        Delete an existing comment.

        Returns:
            dict: A dictionary containing a message indicating the deletion status.
        """# noqa
        try:
            Comments.delete_comment(self.comment_id)
            return {"data": [{"message": "Comment deleted successfully"}]}
        except Exception as e:
            raise e
