
from app.api.models.models import User


class SericeHelper():

    @staticmethod
    def create_post_res(posts):
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
    def is_user_exists(username):
        return User.query.filter_by(username=username).first()
