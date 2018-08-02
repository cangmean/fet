from fet.tools.alioss import ALIOSS


def test_alioss_upload(app):
    # 测试上传文件
    app.config.setdefault('FET_OSS_ACCESS_ID', '')
    app.config.setdefault('FET_OSS_ACCESS_SECRET', '')
    app.config.setdefault('FET_OSS_INTERNAL_URL', '')
    app.config.setdefault('FET_OSS_EXTERNAL_URL', '')
    app.config.setdefault('FET_OSS_BUCKET_NAME', '')
    alioss = ALIOSS(app)
    url = alioss.bucket.upload_file(
        'hea.jpg', 'head.jpg'
    )
    assert url == alioss.bucket.make_url('hea.jpg')