import oss2


class Bucket(object):

    def __init__(
        self, access_id, access_secret, internal_url=None,
        external_url=None, bucket_name=None
    ):
        auth = oss2.Auth(access_id, access_secret)
        self.internal_url = internal_url
        self.external_url = external_url
        self.bucket_name = bucket_name

        if internal_url:
            url = internal_url
        elif external_url:
            url = external_url
        else:
            raise ValueError('Url not exists.')
        self.bucket = oss2.Bucket(auth, 'http://' + url, bucket_name)

    def make_url(self, name):
        """ 生成url"""
        url = 'http://{}.{}/{}'.format(
            self.bucket_name,
            self.external_url,
            name
        )
        return url

    def upload_file(self, name, path):
        """ 上传文件
        :param name: 远程文件路径名称比如  /a/b/iu.jpeg
        :param path: 本地上传文件路径
        """
        try:
            self.bucket.put_object_from_file(name, path)
            img_url = self.make_url(name)
            return img_url
        except Exception as e:
            print(e)

    def upload_data(self, name, data):
        """ 上传数据"""
        try:
            self.bucket.put_object(name, data)
            img_url = self.make_url(name)
            return img_url
        except Exception as e:
            pass

    def down_file(self, name, path):
        """ 下载文件
        :param name: 远程文件路径
        :param path: 本地文件路径
        """
        try:
            self.bucket.get_object_to_file(
                name, path,
            )
        except Exception as e:
            print(e)

    def down_file_data(self, name):
        """ 下载文件二进制数据
        :param name: 远程文件路径
        """
        try:
            stream = self.bucket.get_object(name)
            return stream
        except Exception as e:
            print(e)

    def delete_one(self, key):
        self.bucket.delete_object(key)

    def delete_many(self, keys):
        for del_keys in group(keys, 1000):
            self.bucket.batch_delete_objects(del_keys)


class AliOss(object):

    def __init__(self, app=None):
        self.bucket = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        
        app.extensions['fet_oss'] = self
