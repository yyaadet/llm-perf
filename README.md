# llm-perf
LLM performance auto test. Get insight and replay evaluation with a little time.

## 运行Kimi测试

- `cd llm-perf`
- `pip install -r requirements.txt`
- 修改`test_kimi.sh`里面的token与cookie值

使用Safari或Chrome登陆进网站: `https://kimi.moonshot.cn`, 随便输入一个文字，用来启动一个新会话。如下图：

![](./snapshots/kimi_help.png)

用新的token、cookie、chat_id替换脚本`test_kimi.sh`里面的值

## 查看报告kimi报告

- `cd streamlit`
- `pip install -r requirements.txt`
- `streamlit run llm_perf.py`

## 友情赞助

![](./snapshots/weixin_donate.JPG)

![](./snapshots/zhifubao_donate.JPG)