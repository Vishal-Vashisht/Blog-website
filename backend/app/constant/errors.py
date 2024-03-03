ERRORS = {
    "INTERNAL_SERVER_ERROR": {
        'ERRORS': [
            {'DETAIL': 'Internal server error'}
        ]
    },
    "POST_ID_REQU": {
        'ERRORS': [
            {'DETAIL': 'post_id : post Id is required'}
        ]
    },
    "POSTID_CONTENT_REQU": {
        'ERRORS': [
            {'DETAIL': 'post Id and content is required'}
        ]
    },
    "POST_CONTENT_IS_SHORT": {
        'ERRORS': [
            {'DETAIL': 'Post content is too short'}
        ]
    },
    "POST_NOT_FOUND": {
        'ERRORS': [
            {"DETAIL": "Post not found"}
        ]
    },
    "USER_EXISTS": {
        'ERRORS': [
            {"DETAIL": "User already exists"}
        ]
    },
    "SHORT_PASS_LEN": {
        'ERRORS': [
            {"DETAIL": "Password must be 8 character long"}
        ]
    },
    "USER_NAME_AND_PASS_REQUIRED": {
        'ERRORS': [
            {"DETAIL": "username and password is required"}
        ]
    },
    "USER_DOES_NOT_EXISTS": {
        'ERRORS': [
            {"DETAIL": "User not exists"}
        ]
    },
    "INVALID_CREDNTIALS": {
        'ERRORS': [
            {"DETAIL": "Invalid credntials"}
        ]
    },
    "COMMENT_POST_ID_REQUIRED": {
        'ERRORS': [
            {"DETAIL": "Comment and post id is required"}
        ]
    },
    "COMMENT_IS_SHORT": {
        'ERRORS': [
            {"DETAIL": "Comment is too short"}
        ]
    },
    "INVALID_POST": {
        'ERRORS': [
            {"DETAIL": "Can't comment on this post"}
        ]
    },
    "COMMENT_ID_NOT_PROVIDED": {
        'ERRORS': [
            {"DETAIL": "Comment and comment id not provided"}
        ]
    },
    "INVALID_COMMENT": {
        "ERRORS": [
            {"DETAIL": "Invalid comment"}
        ]
    },
    "COMMENTID_NOT_PROVIDED": {
        'ERRORS': [
            {"DETAIL": "Comment id not provided"}
        ]
    },
}


JWT_ERRORS = {
    "JWT_TOKEN_EXPIRED": {
        'ERRORS': [
            {"DETAIL": "Token has expired"}
        ]
    },
    "JWT_TOKEN_INVALID": {
        'ERRORS': [
            {"DETAIL": "Token is invalid"}
        ]
    },
    "JWT_AUTH_REQUIRED": {
        'ERRORS': [
            {"DETAIL": "Authorization Required"}
        ]
    },
}
