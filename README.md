# 在线剪贴板

一个基于Django开发的在线剪贴板应用，支持文本和文件的快速分享。

## 功能特点

- 创建独立的剪贴板空间，支持可选密码保护
- 支持文本内容和文件的上传与分享
- 管理员后台支持剪贴板内容管理
- 自动记录创建和修改时间
- 支持按类型、时间等多维度筛选内容

## 技术栈

- Python 3.12+
- Django 5.1.4
- SQLite 数据库
- Django Admin 后台管理

## 项目结构

```
├── board/                  # 主应用目录
│   ├── migrations/         # 数据库迁移文件
│   ├── templates/         # 模板文件
│   ├── admin.py           # 后台管理配置
│   ├── models.py          # 数据模型
│   └── views.py           # 视图函数
├── clipboard/             # 项目配置目录
├── media/                 # 媒体文件目录
│   └── board_files/       # 上传文件存储目录
└── manage.py             # Django管理脚本
```

## 数据模型

### Board（剪贴板）
- identifier: 唯一标识符
- password: 可选密码保护
- is_admin_created: 是否管理员创建
- admin_notes: 管理员备注
- created_at: 创建时间
- last_modified: 最后修改时间

### BoardItem（剪贴板项目）
- board: 关联的剪贴板
- item_type: 项目类型（文本/文件）
- text_content: 文本内容
- file: 上传的文件
- file_name: 文件名
- mime_type: 文件类型
- created_at: 创建时间
- last_modified: 最后修改时间

## 安装部署

1. 克隆项目到本地

```bash
git clone [项目地址]
cd clipboard
```

2. 创建并激活虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. 安装依赖

```bash
pip install django
```

4. 初始化数据库

```bash
python manage.py migrate
```

5. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

6. 启动开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/ 即可使用应用
访问 http://127.0.0.1:8000/admin/ 进入管理后台

## 使用说明

1. 创建剪贴板：访问首页可创建新的剪贴板空间
2. 添加内容：在剪贴板中可以添加文本或上传文件
3. 分享：通过剪贴板的唯一标识符分享内容
4. 管理：在Django Admin后台可以管理所有剪贴板和内容

## 开发说明

- 文件上传路径配置在 `board/models.py` 中的 `BoardItem` 模型
- 后台管理界面配置在 `board/admin.py`
- 每页显示20条记录的配置在后台管理类中

## 注意事项

- 请定期清理媒体文件目录下的旧文件
- 生产环境部署时请修改 `SECRET_KEY` 和 `DEBUG` 设置
- 建议配置更安全的数据库和文件存储方案