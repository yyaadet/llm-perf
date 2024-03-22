import streamlit as st
import pandas as pd
from pathlib import Path
import os

base_dir = Path(os.path.dirname(__file__))
kimi_csv = base_dir / "../reports/kimi_2024_03_22.csv"

st.title("LLM Performance Report")
st.caption("@yyaadet2002 发布，仅供学习研究，邮件联系 yyaadet@qq.com")

st.header("Kimi CEval数据测试")

kimi_df = pd.read_csv(str(kimi_csv))
kimi_df = kimi_df[kimi_df['chat_answer'].isna() == False]

# accuracy
accuracy = len(kimi_df[kimi_df['is_right'] == True]) / len(kimi_df)
st.text(f"准确率: {round(accuracy * 100, 4)}%，测试数据{len(kimi_df)}条")

avg_speed = kimi_df["output_speed"].mean()
st.text(f"平均响应速度（字/秒）：{round(avg_speed, 2)}")

avg_output_length = kimi_df['output_length'].mean()
avg_input_length = kimi_df['input_length'].mean()
output_input_ratio = avg_output_length / avg_input_length
st.text(f"平均输入长度：{round(avg_input_length, 2)}字, 回答平均长度：{round(avg_output_length, 2)}字，回答/问题长度比：{round(output_input_ratio, 2)}")

st.subheader("测试数据详情")
st.dataframe(kimi_df)

