from app.api.models.models import db, Posts, Likes


class PostLikeDislike():
    def __init__(self, data) -> None:
        self.data = data
        self.user_id = 1

    def post_like_dislike_process(self):

        try:
            # Get the post id
            post_id = self.data.get("post_id")

            # Get the post which we want to like
            post = Posts.query.get(post_id)

            # get the like post
            liked_instance = Likes.query.filter_by(
                post_id=post_id, liked_by=self.user_id).first()

            # Check post is already liked then dislike it
            if liked_instance:
                post.likes -= 1
                liked_instance.delete_()

            # Like it
            else:
                post.likes += 1
                Likes.post_liked(post.post_id, self.user_id)

            db.session.commit()
            return {
                "data": [{"total_likes": post.likes}]
            }

        except Exception as e:
            raise e
