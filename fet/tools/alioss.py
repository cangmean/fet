import oss2
import oss2.exceptions
import logging

logger = logging.getLogger('alioss')


def group(data, size):
    ret = []
    for i in data:
        ret.append(i)
        if len(ret) == size:
            yield ret
            ret = []
    else:
        yield ret


class Bucket(object):

    def __init__(
        self,
        access_id,
        access_secret,
        internal_url=None,
        external_url=None,
        bucket_name=None,
        protocol='http',
    ):
        auth = oss2.Auth(access_id, access_secret)
        self.internal_url = internal_url
        self.external_url = external_url
        self.bucket_name = bucket_name
        self.protocol = protocol

        if internal_url:
            url = internal_url
        elif external_url:
            url = external_url
        else:
            raise ValueError('Url not exists.')

        if not url.startswith(protocol):
            url = protocol + '://' + url

        self.bucket = oss2.Bucket(auth, url, bucket_name)

    def make_url(self, name):
        """ 生成访问url"""
        url = '{protocol}://{bucket}.{url}/{name}'.format(
            protocol=self.protocol,
            bucket=self.bucket_name,
            url=self.external_url,
            name=name
        )
        return url

    def is_exists(self, name):
        """ 判断是否存在
        :param name: 远程文件路径
        """
        return self.bucket.object_exists(name)

    def get_filenames(self, prefix='/'):
        """ 获取某一个路径下的所有文件
        :param prefix: 下载路径的前缀, 比如 fun/ 表示获取fun/目录下所有的文件
        """
        items = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
            items.append(obj.key)
        return items

    def upload_file(self, name, path):
        """ 上传文件
        :param name: 远程文件路径名称比如  /a/b/iu.jpeg
        :param path: 本地上传文件路径
        """
        try:
            res = self.bucket.put_object_from_file(name, path)
            if res.status == 200:
                img_url = self.make_url(name)
                return img_url
        except Exception as e:
            logger.error(str(e))

    def upload_data(self, name, data):
        """ 上传数据"""
        try:
            res = self.bucket.put_object(name, data)
            if res.status == 200:
                img_url = self.make_url(name)
                return img_url
        except Exception as e:
            logger.error(str(e))

    def down_file(self, name, path):
        """ 下载文件
        :param name: 远程文件路径
        :param path: 本地文件路径
        """
        try:
            self.bucket.get_object_to_file(
                name, path,
            )
        except oss2.exceptions.NoSuchKey as e:
            logger.error('Not Found Key: {}'.format(name))
        except Exception as e:
            logger.error(str(e))

    def down_file_data(self, name):
        """ 下载文件二进制数据
        :param name: 远程文件路径
        """
        try:
            res = self.bucket.get_object(name)
            if res.status == 200:
                return res.stream.read()
        except oss2.exceptions.NoSuchKey as e:
            logger.error('Not Found Key: {}'.format(name))
        except Exception as e:
            logger.error(str(e))

    def delete_one(self, name):
        try:
            self.bucket.delete_object(name)
        except oss2.exceptions.NoSuchKey as e:
            logger.error('Not Found Key: {}'.format(name))
        except Exception as e:
            logger.error(str(e))

    def delete_many(self, names, size=1000):
        for del_names in group(names, size):
            self.bucket.batch_delete_objects(del_names)


class ALIOSS(object):

    def __init__(self, app=None):
        self.bucket = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.config.setdefault('FET_OSS_ACCESS_ID', None)
        app.config.setdefault('FET_OSS_ACCESS_SECRET', None)
        app.config.setdefault('FET_OSS_INTERNAL_URL', None)
        app.config.setdefault('FET_OSS_EXTERNAL_URL', None)
        app.config.setdefault('FET_OSS_BUCKET_NAME', None)

        app.extensions['fet_oss'] = self
        if not self.bucket:
            self.bucket = self.get_bucket(app)

    def get_bucket(self, app):
        bucket = Bucket(
            app.config['FET_OSS_ACCESS_ID'],
            app.config['FET_OSS_ACCESS_SECRET'],
            internal_url=app.config['FET_OSS_INTERNAL_URL'],
            external_url=app.config['FET_OSS_EXTERNAL_URL'],
            bucket_name=app.config['FET_OSS_BUCKET_NAME'],
        )
        return bucket
