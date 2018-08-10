### 阿里 oss 扩展

Flask alioss 扩展

#### 添加扩展

通过设置配置可以使用

```python
from fet.tools.alioss import ALIOSS
from flask import Flask

app = Flask(__name__)
app.config.setdefault('FET_OSS_ACCESS_ID', '')
app.config.setdefault('FET_OSS_ACCESS_SECRET', '')
app.config.setdefault('FET_OSS_INTERNAL_URL', '')
app.config.setdefault('FET_OSS_EXTERNAL_URL', '')
app.config.setdefault('FET_OSS_BUCKET_NAME', '')
alioss = ALIOSS(app)

url = alioss.bucket.upload_file(
    'head.jpg', 'head.jpg'
)
```
