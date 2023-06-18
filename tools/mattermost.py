from mattermostdriver.driver import Driver
from django.conf import settings


def mattermost_post_in_channel_manager(
        msg, channel_name, team_name, file_path, msg_type='text', username_list=None, is_pinned=True, *args, **kwargs
):
    driver = mattermost_connection()
    mattermost_login(driver)
    channel_obj = mattermost_get_channel(driver, channel_name=channel_name, team_name=team_name)
    user_ids = mattermost_get_user_ids_from_usernames(driver=driver, username_list=username_list)

    if not channel_obj:
        team_id = mattermost_get_team_by_name(driver, team_name)
        channel_obj = mattermost_create_channel(driver, team_id, channel_name)
    are_added, failed_to_create_users = mattermost_add_users_to_channel(driver, channel_obj.get("id"), user_ids)
    if isinstance(channel_obj, dict):
        mattermost_post_in_channel(
            driver=driver, channel_id=channel_obj.get("id"), msg=msg,
            msg_type=msg_type, file_path=file_path, is_pinned=is_pinned
        )
    return True


def mattermost_connection(url=None, token=None, *args, **kwargs):
    driver = Driver({
        'url': 'im.dkservices.ir',
        "token": settings.MM_TOKEN,
        'scheme': 'https',
        'port': 443
    })
    return driver if driver else False


def mattermost_login(driver):
    try:
        result = driver.login()
        return result if result else False
    except Exception as e:
        return False


def mattermost_get_team_by_name(driver, team_name):
    try:
        return driver.teams.get_team_by_name(team_name).get('id')
    except Exception as e:
        return False


def mattermost_get_channel(driver, channel_name, team_name):
    try:
        channel = driver.channels.get_channel_by_name_and_team_name(team_name, channel_name)
        return channel
    except Exception as e:
        return False


def mattermost_get_user_ids_from_usernames(driver, username_list):
    try:
        user_ids = []
        users_obj_list = driver.users.get_users_by_usernames(options=username_list)
        [user_ids.append(user.get('id')) for user in users_obj_list if user]
        return user_ids
    except Exception as e:
        return False


def mattermost_create_channel(driver, team_id, channel_name):
    try:
        return driver.channels.create_channel(options={
            "team_id": team_id,
            "name": channel_name,
            "display_name": channel_name,
            "purpose": "Business Continuity Management Group",
            "header": "Business Continuity Management",
            "type": "P"  # Private Channel
        })
    except Exception as e:
        return False


def mattermost_add_users_to_channel(driver, channel_id, user_ids):
    try:
        failed_usernames = []
        for user_id in user_ids:
            try:
                driver.channels.add_user(channel_id, options={'user_id': user_id})
            except Exception as e:
                failed_usernames.append(driver.users.get_user(user_id).get('username'))

        return True, failed_usernames
    except Exception as e:
        return {}


def mattermost_post_in_channel(driver, channel_id, msg, file_path, is_pinned, msg_type='text'):
    post = {}
    try:
        if channel_id:
            if msg_type == 'text':
                post = driver.posts.create_post(options={
                    'channel_id': channel_id,
                    'message': msg
                })
                if is_pinned:
                    driver.posts.pin_post_to_channel(post_id=post.get('id'))

            elif msg_type == 'file':
                form_data = {
                    "channel_id": ('', channel_id),
                    "client_ids": ('', "id_for_the_file"),
                    "files": (file_path, open(file_path, 'rb')),
                }
                file_post = driver.files.upload_file(channel_id, form_data)
                file_id = file_post.get("file_infos")[0].get("id")
                driver.posts.create_post(options={
                    'channel_id': channel_id,
                    'message': 'Hi...',
                    "file_ids": [file_id]
                })

            return True if post else False
    except Exception as e:
        return False