# fet

flask extensions tools

### 安装

通过`git clone`源码安装

```bash
git clone https://github.com/cangmean/fet.git
python setup.py install
```

使用`pip`安装

```bash
pip install git+https://github.com/cangmean/fet.git
```

也可以添加到`requirements.txt`中

```bash
git+https://github.com/cangmean/fet.git
```

### 修改 Flask 默认打印信息

修改默认 Flask 打印信息，添加响应耗时(不是特别精准，只能在测试环境下当参考)

```python
from fet import _Flask as Flask

app = Flask(__name__)
...

app.run(debug=True)
```

显示效果

```bash
[INFO] [2018-08-10 12:56:22] "GET / HTTP/1.1" 200 rtime = 29.23 ms
[INFO] [2018-08-10 12:56:22] "GET /favicon.ico HTTP/1.1" 404 rtime = 156.93 ms
```
