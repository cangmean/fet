### session 扩展

Flask session 扩展

#### 添加扩展

```python
from fet.tools.session import Session
from flask import Flask

app = Flask(__name__)
app.config.setdefault('FET_SESSION_STORE', None)
app.config.setdefault('FET_SESSION_NAME', None)
app.config.setdefault('FET_SESSION_EXPIRES', None)
session = Session(app)

session.set('name', 'mink')
session.get('name')
session.exists('name')
```
