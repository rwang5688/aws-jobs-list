import s3util


def get_task_attribute_value(task, task_attribute_name):
    task_attribute_value = ''
    if task_attribute_name in task:
        task_attribute_value = task[task_attribute_name]
    else:
        print('get_task_attribute_value: Task attribute %s is not defined.' % task_attribute_name)

    return task_attribute_value


def get_task_file_blob(bucket_name, task, task_file_attribute_name):
    # get bucket
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('get_task_file: Bucket %s does not exist.' % bucket_name)
        return None

    # get user_id, task_id, task_file_name
    user_id = get_task_attribute_value(task, 'user_id')
    if user_id == '':
        return None

    task_id = get_task_attribute_value(task, 'task_id')
    if task_id == '':
        return None

    task_file_name = get_task_attribute_value(task, task_file_attribute_name)
    if task_file_name == '':
        return None

    # get $(user_id)/$(task_id)/task_file_name
    task_file_object_name = user_id + "/" + task_id + "/" + task_file_name
    task_file_object = s3util.get_file_object(bucket_name, task_file_object_name)
    if task_file_object is None:
        print('get_task_file: Failed to get scan file object %s' % task_file_object_name)
        return None

    # success
    task_file_blob = task_file_object['Body'].read()
    return task_file_blob


def download_task_file(bucket_name, task, task_file_attribute_name):
    # get bucket
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('download_task_file: Bucket %s does not exist.' % bucket_name)
        return ''

    # get user_id, task_id, task_file_name
    user_id = get_task_attribute_value(task, 'user_id')
    if user_id == '':
        return ''

    task_id = get_task_attribute_value(task, 'task_id')
    if task_id == '':
        return ''

    task_file_name = get_task_attribute_value(task, task_file_attribute_name)
    if task_file_name == '':
        return ''

    # download $(user_id)/$(task_id)/task_file_name
    object_key = user_id + "/" + task_id + "/" + task_file_name
    success = s3util.download_file(bucket_name, object_key, task_file_name)
    if not success:
        print('download_task_file: Failed to download task file %s.' % task_file_name)
        return ''

    # success
    return task_file_name


def upload_task_file(bucket_name, task, task_file_attribute_name):
    # get bucket
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('upload_task_file: Bucket %s does not exist.' % bucket_name)
        return False

    # get user_id, task_id, task_file_name
    user_id = get_task_attribute_value(task, 'user_id')
    if user_id == '':
        return False

    task_id = get_task_attribute_value(task, 'task_id')
    if task_id == '':
        return False

    task_file_name = get_task_attribute_value(task, task_file_attribute_name)
    if task_file_name == '':
        return False

    # upload task file
    success = s3util.upload_file(task_file_name, bucket["Name"], user_id + "/" + task_id + "/" + task_file_name)
    if not success:
        print('upload_task_file: Failed to upload task file %s.' % task_file_name)
        return False

    # success
    return True
