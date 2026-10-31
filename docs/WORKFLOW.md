# 每日研究与发布流程

## 调度与范围

既有Codex定时任务“具身智能与机器人基础模型研究日报”每天北京时间07:00触发，工作目录为本项目。研究主线为统一多模态模型的动作预测，检索同时覆盖VLA、WAM、动作表示、数据、适应、评测与部署，不以缩写或单一路线限制候选。仓库不另设依赖API密钥的定时研究任务。

## 检索、阅读与写作

目录与页面名遵循“arXiv号在前，题目或简称在后”：papers/2610.34356-RynnVLA-Latent/，页面首行“# 2610.34356 · RynnVLA-Latent”，随后给完整英文题目。论文索引papers/README.md、首页列表与catalog按arXiv号升序排列；目录实际路径记录在catalog及metadata的directory字段，不再假设目录名只有ID。

先读data/state.json和历史笔记。搜索自上次成功截止时间以来的更新，再重叠7天补漏；按arXiv ID、DOI和官方仓库去重。区分首发、重要修订、代码、权重与数据发布。精选3至6项，可以更少；不重复旧内容凑数，必要时另列一项旧工作延伸阅读。

查原文、作者项目页和官方仓库，再查对应alphaXiv。alphaXiv是发现和解释的补充，不替代原文。独立撰写中文摘要与AI介绍，使用段落解释方法和证据；只在展示实验数据时用表格。逐篇记录读了哪些章节、是否核查实现、是否运行实验。

优先沿用alphaXiv解读的问题、方法、实验和边界来组织信息，减少重复介绍；未取得明确转载许可时保留链接、中文提炼和简短引用，不全文搬运。若有可转载许可或用户提供的可用全文，记录来源及授权范围，并按GitHub Markdown整理：标题、段落、列表、标准$...$与$$...$$公式、本地相对图片链接；移除依赖网页脚本、iframe或登录态的展示。当前[alphaXiv条款](https://www.alphaxiv.org/terms)未提供整篇公开转载许可（核查于2026-10-30）。

语言首选为zh。使用https://www.alphaxiv.org/zh/abs/<arxiv-id>并核查AI Overview正文为中文，记录language、检查状态与时间；不要把英文原文的自译标成网站中文原文。目录、日报及逐篇来源链接统一指向已验证的中文版。缺失时如实标注，不回退后仍声称已读中文版。用户仅用于个人阅读与总结；仓库可见性仍沿用已确认设置。

日报保存reports/YYYY/MM/DD.md，约1500至2500字；完整逐篇笔记保存papers/<id>-<short-title>/README.md。作者结论与本项目推断分开，数字带协议和条件，开放状态未核实就写未核实。访问失败必须写缺失范围，不能推断没有新研究。

## 截图与卡片

先把原始PDF存入.cache/<id>/paper.pdf（忽略），在metadata.json登记版本和SHA256。看页面缩略图再选与解释相关的方法/结果图，登记1-based PDF页码及从左上角计量的point坐标[x0,y0,x1,y1]。例如：

```bash
python3 scripts/capture_figures.py --paper 2610.37091
python3 scripts/render_cards.py --font /path/to/CJK-font.ttc
```

截图源文件保留在本地缓存；Git只提交图像摘录。每张图在笔记中有图号、页码和来源。摘要卡片与阅读卡片由本项目自写内容排版，不能冒充alphaXiv网页原图。逐张目视检查文字大小、图边界与对应关系。

PDF下载失败时，可保存arXiv HTML中直接提供的官方原图。元数据kind标为arxiv_html_figure，记录figure_number、原图URL和source_image_sha256；不虚构PDF页码、裁剪坐标或PDF SHA256，正文说明取图方式与PDF缺失。

首次依赖可用python3 -m pip install -r requirements.txt安装；已提供Codex运行时依赖时优先复用，不修改用户全局环境。Markdown校验与Git发布只需Python标准库和Git。

## 状态与发布

更新data/catalog.json、成功检索边界和README最新索引。只有完成检索及报告才推进边界；来源失败保留补查区间。补充旧报告不推进边界。Git失败不回滚已完成的文档，也不能报成已发布。

```bash
python3 scripts/validate.py
python3 scripts/publish.py --message "docs: add YYYY-MM-DD research reading"
```

脚本先校验、fetch和ff合并，只暂存档案白名单路径，不强推。远程冲突、认证问题或未配置origin时停止并报告。成功后比较本地HEAD与远程分支SHA，回复直接报告与commit链接。不要重复创建仓库，不删除用户文件，不把凭据、缓存或完整论文放入Git。
