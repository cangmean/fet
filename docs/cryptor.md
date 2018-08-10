### AES 加密解密

Flask AES 扩展

#### 添加扩展

```python
from fet.tools.cryptor import Cryptor
from flask import Flask

app = Flask(__name__)
app.config.setdefault('FET_AES_SECRET_KEY', '')
cryptor = Cryptor(app)
x = cryptor.encrypt('123123', salt='hello')
y = cryptor.decrypt(x, salt="hello")
assert x == '123123'
```
