# running-coach-skill — 跑步训练方法论知识库（Kai/Anthropic Skill）

把 7 本经典跑步/体能书的方法论蒸馏成 AI 可套用的**程序化训练知识**（强度分区、周期化、
跑姿、力量、拉伸、伤痛预防、马拉松方法），供 Kai（支持 SKILL.md 的客户端）当作权威知识库使用。

## 在 Kai 里安装

**Skills → Add Skill**，粘贴（技能在 `skills/running-coach-library/` 子目录下，必须带该路径子目录才会把 `references/`、`scripts/` 一起装进沙盒）：

```
ly-ly-666/running-coach-skill/skills/running-coach-library
```

或完整 URL：

```
https://github.com/ly-ly-666/running-coach-skill/tree/main/skills/running-coach-library
```

装好后，在对话里用斜杠命令触发（id 来自 SKILL.md frontmatter 的 `name`）：

```
/running-coach-library 给一个针对 10 公里比赛的中周期训练安排
```

> 提示：Kai 安装技能走**未认证 GitHub API**（不带 token），因此本仓库为 **public**。
> 需在**已装好 Linux 沙盒的 Android 端**操作。

## 仓库结构

```
skills/running-coach-library/
├── SKILL.md               # 技能入口（frontmatter: name/description）
├── README.md              # 技能说明
├── references/            # 7 本书蒸馏知识（按需加载）
│   ├── daniels.md         #   丹尼尔斯 VDOT + E/M/T/I/R 强度体系
│   ├── periodization.md   #   邦帕周期训练
│   ├── injuryfree.md      #   无伤跑法
│   ├── pose.md            #   姿势跑法
│   ├── stretching.md      #   拉伸系统训练（动态/静态/PNF）
│   ├── nsca.md            #   NSCA 力量训练指南（OCR 提取）
│   └── hansons.md         #   汉森马拉松训练法（OCR 提取）
└── scripts/
    └── search_knowledge.py # 中英文混合确定性检索
```

## 数据源与精度

- **5 本有文本层**（daniels/periodization/injuryfree/pose/stretching）：pdfplumber 全书提取后蒸馏，附「来源映射」可回溯。
- **2 本扫描版**（hansons/nsca）：tesseract(chi_sim) **逐页 OCR** 后整理；关键配速/距离/负荷数字已逐处人工核对，OCR 可能有少量错字。
- 本库提供"如何做"的方法论（流程/决策规则/反模式/速查表），非原文检索；需精准定位用 `scripts/search_knowledge.py`。