# OpenClaw Project Manager Skill
一个开箱即用的项目全生命周期管理Skill，专为OpenClaw AI助手设计，支持任务自动拆解、动态进度跟踪、风险智能识别、报告自动生成，可无缝对接飞书日历/群聊协作。

## ✨ 核心功能
| 功能 | 说明 |
|------|------|
| 📋 任务自动拆解 | 输入项目目标、时间范围、负责人列表，自动生成结构化任务清单，包含每个任务的Owner、DDL、交付物、验收标准 |
| 📊 进度动态管理 | 支持实时更新任务进度，自动计算整体项目完成率 |
| ⚠️  风险智能识别 | 自动识别逾期任务、即将到期未启动任务，给出预警和解决方案建议 |
| 📑 报告自动生成 | 一键生成周进度报告、项目最终复盘报告，支持Markdown格式导出 |
| 📅 飞书生态对接 | 自动同步任务到飞书日历、支持群内@负责人跟进、自动推送进度提醒 |
| 💾 数据持久化 | 所有项目数据自动存储，随时可查询、可追溯 |

## 🚀 快速开始
### 环境要求
- OpenClaw >= 0.8.0
- Python >= 3.8
- 已配置飞书权限（可选，用于日历/群消息推送）

### 安装
1. 将本项目放到OpenClaw的Skill目录下：
```bash
mv project-manager ~/.openclaw/skills/
```
2. 给脚本添加执行权限：
```bash
chmod +x ~/.openclaw/skills/project-manager/scripts/*.py
```

### 使用方式
#### 自然语言调用（推荐）
直接对OpenClaw说：
> "帮我管理清北招聘项目，时间3月12日到3月31日，负责人是庄凯芸、王恂"
> 
> "清北招聘项目T01任务已经完成100%，需求对齐完成"
> 
> "给我生成清北招聘项目本周的进度报告"

#### 命令行调用
```bash
# 1. 初始化项目
cd ~/.openclaw/skills/project-manager/scripts
python task_split.py "清北招聘项目突破" "2026-03-12至2026-03-31" "庄凯芸,王恂"

# 2. 查看项目进度
python progress_tracker.py show <项目ID>

# 3. 更新任务进度
python progress_tracker.py update <项目ID> T01 100 "需求对齐完成"

# 4. 检查项目风险
python progress_tracker.py check_risk <项目ID>

# 5. 生成周进度报告
python report_generator.py <项目ID> weekly

# 6. 生成项目复盘报告
python report_generator.py <项目ID> final
```

## 📁 项目结构
```
project-manager/
├── SKILL.md          # Skill核心配置文件（OpenClaw自动读取）
├── README.md         # 项目说明文档
├── .gitignore        # Git忽略配置
├── scripts/          # 核心脚本
│   ├── task_split.py       # 任务自动拆解脚本
│   ├── progress_tracker.py # 进度跟踪脚本
│   └── report_generator.py # 报告生成脚本
└── references/       # 数据存储目录
    └── projects/           # 项目数据存储位置（每个项目一个JSON文件）
```

## 🎯 使用场景
1. 个人项目管理：自动拆解任务、跟踪进度、生成复盘报告
2. 团队项目协作：拉到群内自动同步进度、@负责人跟进任务、风险预警
3. 多项目并行管理：同时管理多个项目，自动同步所有项目进度
4. 定期汇报：自动生成周/月报，节省汇报时间

## 🤝 贡献
欢迎提交Issue和PR，有任何功能建议或者问题都可以提。

## 📄 许可证
MIT License
