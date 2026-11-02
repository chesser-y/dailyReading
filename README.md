# dailyReading

具身智能与机器人基础模型阅读档案。主线是**统一多模态模型的动作预测能力**，开放覆盖VLA、WAM、动作表示、视频预测、数据规模化、后训练、评测与部署。

每日北京时间 **07:00（Asia/Shanghai）** 由Codex已配置的定时研究任务检索、阅读、归档并提交。定时执行器在Codex中；仓库内的脚本负责文档校验、截图与Git发布。

## 最新阅读

[2026-11-02 日报](reports/2026/11/02.md)：ThinkWorld世界一致性训练、SPT偏好自标注、DEED数据与执行设计；另补查PDRVLA v2与Cosmos3转换记录。

[2026-11-01 日报](reports/2026/11/01.md)：E0.5未来几何目标、Cross-Controller交互上下文与AcrossDEX动作块连续性；三篇近7天补漏，均已读zh概述。

[2026-10-31 日报](reports/2026/10/31.md)：GAR高斯读出、CoAWM连续时间动作、RoboAtom技能监督与WorldProbe长时一致性。四篇均为7天补漏，zh AI概述已读取。

[2026-10-30 首期日报](reports/2026/10/30.md)：潜在动作预训练、紧凑世界模型与反事实策略改进。

- [2610.34356 · RynnVLA-Latent](papers/2610.34356-RynnVLA-Latent/README.md)
- [2610.36011 · E0.5](papers/2610.36011-E0.5/README.md)
- [2610.36068 · Rollback](papers/2610.36068-Rollback/README.md)
- [2610.36791 · RynnWorld-Latent](papers/2610.36791-RynnWorld-Latent/README.md)
- [2610.37091 · GAWM](papers/2610.37091-GAWM/README.md)
- [2610.37381 · PDRVLA](papers/2610.37381-PDRVLA/README.md)
- [2610.37666 · ThinkWorld](papers/2610.37666-ThinkWorld/README.md)
- [2610.38000 · SPT](papers/2610.38000-SPT/README.md)
- [2610.39280 · Cross-Controller](papers/2610.39280-Cross-Controller/README.md)
- [2610.39721 · WorldProbe](papers/2610.39721-WorldProbe/README.md)
- [2610.40207 · RoboAtom](papers/2610.40207-RoboAtom/README.md)
- [2610.40210 · AcrossDEX](papers/2610.40210-AcrossDEX/README.md)
- [2610.40271 · GAR](papers/2610.40271-GAR/README.md)
- [2610.40401 · CoAWM](papers/2610.40401-CoAWM/README.md)
- [2610.40430 · DEED](papers/2610.40430-DEED/README.md)

[按arXiv号浏览全部论文](papers/README.md)

## 阅读方式

每篇包含中文摘要、AI撰写介绍、输入→处理→输出、关键设计、论文方法图截图、实验证据、局限、研究借鉴及alphaXiv解读补充。**除实验数据外，使用段落和少量列表，不使用大表格承载解释。**

阅读程度逐篇标注。原文作者结论、alphaXiv解读与本项目推断分开；未读全文、未核查代码、未复现实验会直说。摘要与阅读卡片为自写内容的排版图；方法图来自PDF局部截图或arXiv HTML官方原图；按实际取图方式记录来源、图号、页码/裁剪坐标或原图哈希。

alphaXiv优先使用 **zh中文版AI Overview**，链接格式为`https://www.alphaxiv.org/zh/abs/<arxiv-id>`。中文原文与本项目摘要/自译明确区分；中文版缺失时如实说明。10月30日笔记最初基于英文版，10月31日新增笔记已读取zh AI概述；实际语言与检查状态记录在各篇metadata.json中。

## 目录

```text
reports/YYYY/MM/DD.md       每日精选与跨论文联系
papers/<arxiv-id>-<short-title>/README.md 逐篇阅读报告
papers/<arxiv-id>-<short-title>/assets/   方法图、摘要卡片、阅读卡片
papers/<arxiv-id>-<short-title>/metadata.json 来源、版本、阅读程度与图像记录
data/catalog.json           可检索论文目录
data/state.json             成功检索边界和去重记录
docs/WORKFLOW.md            每日执行与提交流程
templates/paper.md          新论文笔记模板
scripts/                   截图、卡片排版、链接校验和Git提交
```

## 本地检查与发布

```bash
python3 scripts/validate.py
python3 scripts/publish.py --message "docs: add YYYY-MM-DD research reading"
```

发布脚本仅提交该仓库文档及图像；没有origin时停止，不创建重复仓库，不强推。用法与依赖见[工作流程](docs/WORKFLOW.md)。PDF、网页原始抓取、模型权重和凭据留在忽略的本地缓存中。

## 来源与使用

所有论文附arXiv与alphaXiv链接。第三方图像、论文及解读的权利归其权利人；本项目保存有限图像摘录及独立撰写的研究笔记。数值采用原文对应设置，不跨不同数据量、相机数、任务输入或评估条件直接排名。
