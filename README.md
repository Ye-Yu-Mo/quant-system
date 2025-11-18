# Quant Minimal System

这是一个极简但完整的量化交易回测系统。它的存在是为了教学，展示一个“好品味”的量化系统应该具备的核心要素：**简洁**和**模块化**。

这个仓库是以下博客系列文章的配套代码：
- **知乎专栏**: [量化投资从入门到入土](https://www.zhihu.com/column/c_1967175114308159173)
- **CSDN专栏**: [量化投资从入门到入土](https://blog.csdn.net/ye_yumo/category_13075797.html)

---

## 核心设计哲学

> "烂程序员关心代码。好程序员关心数据结构和它们之间的关系。"

这个系统的设计遵循关注点分离（Separation of Concerns）的原则，确保各个组件职责单一、清晰：

- **数据 (`data.py`)**: 只负责加载数据。它做好一件事就够了。
- **策略 (`strategy/`)**: 包含实际的交易逻辑。它应该独立于数据来源和回测引擎。
- **回测器 (`backtester.py`)**: 驱动整个回测流程的引擎。它接收数据和策略，然后模拟交易过程，产出结果。

数据流是单向的：`数据` -> `回测器` -> `策略`。这种清晰的结构可以避免许多糟糕系统中常见的混乱。

## 项目结构

```
quant-minimal-system/
├── quant/
│   ├── main.py             # 主入口：负责组装和启动系统
│   ├── backtester.py       # 核心回测引擎
│   ├── data.py             # 数据加载模块
│   └── strategy/           # 策略目录
│       └── dca_strategy.py # 示例策略：成本平均法 (DCA)
└── requirements.txt        # 项目依赖
```

- `quant/main.py`: 唯一的入口。它的职责就是启动程序，不要在这里塞满逻辑。
- `quant/backtester.py`: 核心回测引擎。
- `quant/data.py`: 数据处理模块。
- `quant/strategy/`: 你自己的交易想法应该放在这里。
- `requirements.txt`: 项目的依赖。一个项目必须明确声明它需要什么才能运行。

## 如何运行

#### 1. 克隆仓库
```bash
git clone https://github.com/Ye-Yu-Mo/quant-minimal-system.git
cd quant-minimal-system
```

#### 2. 创建并激活虚拟环境 (推荐)
一个干净的环境是良好工程实践的开端。
```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.\.venv\Scripts\activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 运行回测
```bash
python -m quant.main
```

## 相关资源

- **博客文章**:
  - 知乎: [量化投资从入门到入土](https://www.zhihu.com/column/c_1967175114308159173)
  - CSDN: [量化投资从入门到入土](https://blog.csdn.net/ye_yumo/category_13075797.html)
- **配套博客项目**:
  - GitHub: [Ye-Yu-Mo/quant-from-zero](https://github.com/Ye-Yu-Mo/quant-from-zero)
  - 网站: [https://ye-yu-mo.github.io/quant-from-zero/](https://ye-yu-mo.github.io/quant-from-zero/)
