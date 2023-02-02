from dbconfig import User


def get_user_by_id(user_id):
    try:
        return User().get(vk_id=user_id)
    except:
        User(vk_id=user_id,warns=0, mute=0, admin = 0).save()
        return User().get(vk_id=user_id)

    