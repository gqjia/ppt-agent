# API PPT Agent

一个基于smolagents的智能代理项目，集成了网页检索工具，能够获取实时信息并生成相关内容。

## 项目特性

- 🤖 基于smolagents的智能代理
- 📊 集成了PPT任务规划智能体（Planner Agent）
- 🌐 集成了强大的网页检索工具
- 📰 支持新闻搜索和网页内容获取
- 🔧 完善的错误处理和重试机制
- 📝 自动内容清理和格式化
- 🎯 智能任务分解和分配

## 核心组件

### 1. Planner Agent（任务规划智能体）

项目包含了一个智能的PPT任务规划智能体，位于 `src/agents/planner_agent.py`。

#### 主要功能
- **需求分析**: 分析PPT项目需求和要求
- **任务分解**: 将项目拆分成多个可执行的子任务
- **时间估算**: 估算每个任务的完成时间
- **资源分配**: 为任务分配合适的agent
- **时间线规划**: 创建项目时间线
- **计划验证**: 验证任务计划的合理性

#### 任务类型
- `research`: 资料收集和调研
- `content`: 内容撰写和编辑
- `design`: 幻灯片设计和布局
- `image`: 图片生成和处理
- `review`: 审查和编辑
- `assembly`: 最终组装和优化

### 2. 网页检索工具

项目包含了一个功能完善的网页检索工具，位于 `src/tools/web_search.py`。

### 主要功能

1. **网页搜索** (`web_search`)
   - 使用DuckDuckGo搜索引擎
   - 支持可选的网页内容获取
   - 智能内容清理和格式化

2. **新闻搜索** (`search_news`)
   - 专门搜索新闻文章
   - 包含新闻来源、发布日期等信息

3. **网页内容获取** (`fetch_webpage_content`)
   - 获取指定URL的网页内容
   - 自动转换为Markdown格式
   - 支持重试机制

### 快速开始

#### 使用Planner Agent

```python
from src.agents.planner_agent import create_planner_agent

# 创建planner agent
planner = create_planner_agent()

# 创建PPT项目
result = planner.create_ppt_project(
    title="人工智能发展趋势报告",
    topic="AI技术的最新发展和未来趋势",
    target_audience="技术管理者和决策者",
    slide_count=20,
    style_preference="modern",
    requirements=["包含最新数据", "有图表展示", "适合演讲"]
)

print(result)
```

#### 使用网页检索工具

```python
from src.tools.web_search import web_search, search_news, fetch_webpage_content

# 搜索网页信息
result = web_search("Python编程", max_results=5)

# 搜索新闻
news = search_news("人工智能", max_results=3)

# 获取网页内容
content = fetch_webpage_content("https://example.com")
```

## 安装和设置

### 环境要求

- Python 3.13+
- uv (推荐) 或 pip

### 安装依赖

```bash
# 使用uv (推荐)
uv sync

# 或使用pip
pip install -r requirements.txt
```

### 激活虚拟环境

```bash
source .venv/bin/activate
```

## 使用方法

### 1. 基本测试

运行测试脚本验证功能：

```bash
# 测试网页检索工具
python test_web_search.py

# 测试Planner Agent
python test_planner_agent.py
```

### 2. 在smolagents中使用

#### 使用Planner Agent

```python
from smolagents import Agent
from src.agents.planner_agent import create_planner_agent

# 创建planner agent
planner = create_planner_agent()

# 使用planner agent的工具
agent = Agent(
    system_prompt="你是一个PPT项目规划专家，可以帮助用户规划PPT项目。",
    tools=[
        planner.analyze_requirements,
        planner.create_task_breakdown,
        planner.assign_tasks_to_agents
    ]
)

# 运行对话
response = agent.run("请帮我规划一个关于人工智能的PPT项目")
print(response)
```

#### 使用网页检索工具

```python
from smolagents import Agent
from src.tools.web_search import web_search, search_news, fetch_webpage_content

# 创建智能体
agent = Agent(
    system_prompt="你是一个智能助手，可以使用网页检索工具获取信息。",
    tools=[web_search, search_news, fetch_webpage_content]
)

# 运行对话
response = agent.run("请搜索一下Python的最新信息")
print(response)
```

### 3. 运行示例

```bash
# 运行网页检索工具示例
python example_usage.py

# 运行完整PPT生成系统示例
python example_ppt_system.py
```

## 项目结构

```
api-ppt-agent/
├── src/
│   ├── agents/
│   │   ├── planner_agent.py   # PPT任务规划智能体
│   │   └── __init__.py
│   └── tools/
│       ├── web_search.py      # 网页检索工具
│       └── __init__.py
├── test_web_search.py         # 网页检索工具测试
├── test_planner_agent.py      # Planner Agent测试
├── example_usage.py           # 网页检索工具示例
├── example_ppt_system.py      # 完整PPT生成系统示例
├── pyproject.toml            # 项目配置
├── uv.lock                   # 依赖锁定文件
└── README.md                 # 项目文档
```

## 配置选项

### DuckDuckGo搜索配置

- `region`: 搜索地区（默认"wt-wt"）
- `safesearch`: 安全搜索级别
- `time`: 时间限制
- `backend`: 后端选择

### 网页获取配置

- `timeout`: 请求超时时间（默认10秒）
- `max_retries`: 最大重试次数（默认3次）
- `max_length`: 内容最大长度（默认2000字符）

## 错误处理

工具包含完善的错误处理机制：

- 网络连接错误
- 请求超时
- 无效URL
- 编码错误
- 服务器错误

所有错误都会返回有意义的错误信息，不会导致程序崩溃。

## 注意事项

1. **网络连接**: 工具需要网络连接才能正常工作
2. **请求频率**: 避免过于频繁的请求，以免被限制
3. **内容过滤**: 工具会自动过滤一些无关内容
4. **编码处理**: 工具会尝试自动检测网页编码

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License
