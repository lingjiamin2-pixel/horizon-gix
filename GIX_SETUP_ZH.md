# 清美 GIX Horizon 部署清单

这份仓库已经把 Horizon 改成一套面向约 130 天备考期的信息雷达：每天最多 8 条，分为“GIX 智慧互联与交互设计”和“621 中外美术设计史论素材”两栏，同时生成中英双语页面。每条内容都附带英语一词汇/长难句练习；GIX 内容附 10 分钟手绘转译，史论内容附 5 分钟视觉记忆卡。

当前 GIX Profile 阈值为 6.4，621 史论 Profile 阈值为 6.2。来源覆盖研究机构、Web 标准、交互设计媒体、设计行业、博物馆与艺术史资料、开源创意技术项目和技术社区；较宽的入口仍由 Profile 评分、主题去重和每日 8 条上限控制噪声。

## 还需要你完成的两项必需设置

### 1. 准备你自己的 GitHub 仓库

1. 登录 GitHub，打开原项目 <https://github.com/Thysrael/Horizon>。
2. 点击右上角 **Fork**，仓库名可用 `horizon-gix`，建议先设为 **Public**，这样 GitHub Pages 在免费账户上最省事。
3. 把 Fork 后的仓库网址发给 Codex，例如 `https://github.com/你的用户名/horizon-gix`。Codex 会把本地已经定制好的文件同步进去。

不要把 GitHub 登录密码或个人访问令牌直接发在聊天里。若后续必须授权上传，优先使用已登录的 GitHub 网页完成授权。

### 2. 创建并保存 DeepSeek API Key

1. 打开 <https://platform.deepseek.com/api_keys>，登录后创建一个新 Key。
2. Key 只显示一次，先临时保存在密码管理器中。
3. 进入你的 GitHub 仓库：**Settings → Secrets and variables → Actions → New repository secret**。
4. Name 填 `DEEPSEEK_API_KEY`，Secret 填刚创建的 Key，然后保存。

不要把 Key 写进 `data/config.github.json`、`.env.gix.example`、Issue、提交记录或截图。工作流只从 GitHub Actions Secret 读取它。

## 首次启动

1. 仓库 **Settings → Actions → General → Workflow permissions** 选择 **Read and write permissions** 并保存。
2. 打开 **Actions → GIX Daily Horizon Briefing → Run workflow**，手动跑第一次。
3. 第一次成功后会出现 `gh-pages` 分支。进入 **Settings → Pages**，选择 **Deploy from a branch**，分支选 `gh-pages`，目录选 `/(root)`，保存。
4. Pages 地址通常是 `https://你的用户名.github.io/horizon-gix/`。

自动任务每天北京时间约 05:17 启动。GitHub 定时任务可能有几分钟延迟，属于正常现象。

## 可选：推送到飞书

当前仓库已启用飞书推送，并通过 GitHub Actions Secret 读取 Webhook。若需要重新配置：

1. 在飞书群中添加“自定义机器人”，复制 Webhook 地址。
2. 在 GitHub Actions Secrets 新建 `HORIZON_WEBHOOK_URL`。
3. 将 `data/config.github.json` 中 `webhook.enabled` 改为 `true`。

## 130 天使用规则

- 每天只精读评分最高的 2 条，其余只扫标题；总时长控制在 20-30 分钟。
- 每天任选 1 条完成手绘练习，不要求成稿，重点积累“问题—交互—系统—价值/风险”结构。
- 每周把 621 栏中最有用的 3 个材料抄入自己的时间轴或专题卡，不把新闻雷达当作教材替代品。
- 英语块只做三件事：记 3 个词、拆 1 个长句、口头复述 30 秒。

## 关键文件

- `data/config.github.json`：模型、信息源、每日上限与输出渠道。
- `profiles-gix/`：两套备考评分和生成模板。
- `.github/workflows/daily-summary.yml`：每天的自动运行和 Pages 发布。
- `.env.gix.example`：仅供本地测试参考，不要填入真实密钥后提交。
