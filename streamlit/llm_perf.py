import streamlit as st
import pandas as pd
from pathlib import Path
import os

from dataclasses import dataclass

from sentence_transformers import SentenceTransformer, util




@dataclass
class Performance:
    name: str = ''
    num: int = 0
    accuracy: float = 0.0
    avg_speed: float = 0.0
    avg_output_length: float = 0.0
    avg_input_length: float = 0.0
    output_input_ratio: float = 0.0


base_dir = Path(os.path.dirname(__file__))
cache_folder = base_dir / "cache"
if cache_folder.exists() is False:
    cache_folder.mkdir(parents=True)

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', cache_folder=cache_folder)
kimi_csv = base_dir / "../reports/kimi_2024_03_23.csv"
glm4_csv = base_dir / "../reports/glm4_2024_03_23.csv"
github_url = 'https://github.com/yyaadet/llm-perf'

st.title("LLM Performance Report")
st.caption(f"@yyaadet2002 发布，仅供学习研究，邮件联系 yyaadet@qq.com ; 开源地址：{github_url}")
    
kimi_df = pd.read_csv(str(kimi_csv))
kimi_df = kimi_df[kimi_df['chat_answer'].isna() == False]

glm4_df = pd.read_csv(str(glm4_csv))
glm4_df = glm4_df[glm4_df['chat_answer'].isna() == False]


def get_performance(df, name) -> Performance:
    p = Performance(name=name)
    p.num = len(df)

    # accuracy
    accuracy = len(df[df['is_right'] == True]) / len(df)
    p.accuracy = accuracy

    avg_speed = df["output_speed"].mean()
    p.avg_speed = avg_speed

    avg_output_length = df['output_length'].mean()
    avg_input_length = df['input_length'].mean()
    output_input_ratio = avg_output_length / avg_input_length
    p.avg_output_length = avg_output_length
    p.avg_input_length = avg_input_length
    p.output_input_ratio = output_input_ratio
    return p

def generate_report(p: Performance) -> Performance:
    st.header(f"{p.name} CEval数据测试")

    # accuracy
    st.text(f"准确率: {round(p.accuracy* 100, 4)}%，测试数据{p.num}条")

    st.text(f"平均响应速度（字/秒）：{round(p.avg_speed, 2)}")

    st.text(f"平均输入长度：{round(p.avg_input_length, 2)}字, 回答平均长度：{round(p.avg_output_length, 2)}字，回答/问题长度比：{round(p.output_input_ratio, 2)}")
    return p


def generate_dashboard(performances: list[Performance]):
    '''
    '''
    df = pd.DataFrame(performances)
    df = df.rename(columns={
        'name':"厂商", 
        'num':'测试数据条目', 
        'accuracy':'准确率', 
        'avg_speed':'平均回答速度（字/秒）', 
        'avg_output_length':'平均回答长度（字）', 
        'avg_input_length':'平均输入长度（字）', 
        'output_input_ratio':'回答/问题长度比'
    })
    st.dataframe(df)


def generate_similarity_matrix(performances:list[Performance], dfs:list[pd.DataFrame]):
    st.subheader('答案相似度矩阵')
    matrix = []
    for i, p in enumerate(performances):
        df1 = dfs[i]
        sims = [p.name]
        for j, target in enumerate(performances):
            df2 = dfs[j]
            if i == j:
                sim = 1.0
            else:
                sim = get_avg_similarity(df1, df2)
            sims.append(sim)
        matrix.append(sims)
    
    columns = ['厂商'] + [p.name for p in performances]
    df = pd.DataFrame(matrix, columns=columns)
    st.dataframe(df)



def get_avg_similarity(df1: pd.DataFrame, df2: pd.DataFrame) -> float:
    answers1 = df1['chat_answer']
    embs1 = model.encode(answers1)
    answers2 = df2['chat_answer']
    embs2 = model.encode(answers2)
    sims = []
    max_count = min(len(answers1), len(answers2))
    for i in range(max_count):
        sims.append(float(util.cos_sim(embs1[i], embs2[i]).detach()))

    return sum(sims) / len(sims)
        
    
p1 = get_performance(kimi_df, "Kimi")
p2 = get_performance(glm4_df, "GLM4")

generate_dashboard([p1, p2])
generate_similarity_matrix([p1, p2], [kimi_df, glm4_df])
generate_report(p1)
generate_report(p2)

