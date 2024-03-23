# llm-perf
LLM performance auto test. Get insight and replay evaluation with a little time.
本项目的目标是打造一个从用户使用的角度出发的、可复现的、自动化程度高的大模型效果评测工具。项目将会包括使用的测试数据、测试代码、测试报告。

![](./snapshots/dashboard.png)

## 数据源

- CEval的val数据集

## 支持大模型

- Kimi
- GLM4

## 运行Kimi测试

需要安装有python3.11版本。

- `cd llm-perf`
- `pip install -r requirements.txt`
- 修改`test_kimi.sh`里面的token与cookie值

使用Safari或Chrome登陆进网站: `https://kimi.moonshot.cn`, 随便输入一个文字，用来启动一个新会话。如下图：

![](./snapshots/kimi_help.png)

用新的token、cookie、chat_id替换脚本`test_kimi.sh`里面的值

## 运行GLM4测试


## 查看报告

- `cd streamlit`
- `pip install -r requirements.txt`
- `streamlit run llm_perf.py`

测试结果明细位于`datasets/`

## 友情赞助

![](./snapshots/zhifubao_donate.JPG)