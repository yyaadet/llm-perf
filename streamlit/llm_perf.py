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
kimi_csv = base_dir / "../reports/kimi_2024_03_25.csv"
glm4_csv = base_dir / "../reports/glm4_2024_03_25.csv"
chatgpt_csv = base_dir / "../reports/chatgpt_2024_03_25.csv"
step_csv = base_dir / "../reports/step_2024_03_26.csv"
yiyan_csv = base_dir / "../reports/yiyan_2024_03_27.csv"
minimax_csv = base_dir / "../reports/minimax_2024_03_30.csv"
llama3_8b_csv = base_dir / "../reports/llama3_8b_2024_04_19.csv"
github_url = 'https://github.com/yyaadet/llm-perf'

st.title("LLM Performance Report")
st.caption(f"@yyaadet2002 发布，仅供学习研究，邮件联系 yyaadet@qq.com ; 开源地址：{github_url}")


names = ['ChatGPT', 'Kimi', 'GLM4', '阶跌星辰', '文心一言3.5', 'Minimax', "LLaMA3 8B"]
embeddings = []
dfs = []
for path in [chatgpt_csv, kimi_csv, glm4_csv, step_csv, yiyan_csv, minimax_csv, llama3_8b_csv]:
    df = pd.read_csv(str(path))
    df = df[df['chat_answer'].isna() == False]
    dfs.append(df)
    
    embs = model.encode(df['chat_answer'])
    embeddings.append(embs)
    

def get_performance(df, name) -> Performance:
    p = Performance(name=name)
    p.num = len(df)

    # accuracy
    if len(df) > 0:
        accuracy = len(df[df['is_right'] == True]) / len(df)
    else:
        accuracy = 0.0
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
        embs1 = embeddings[i]
        for j, target in enumerate(performances):
            df2 = dfs[j]
            embs2 = embeddings[j]
            if i == j:
                sim = 1.0
            else:
                sim = get_avg_similarity(df1, embs1, df2, embs2)
            sims.append(sim)
        matrix.append(sims)
    
    columns = ['厂商'] + [p.name for p in performances]
    df = pd.DataFrame(matrix, columns=columns)
    st.dataframe(df)



def get_avg_similarity(df1: pd.DataFrame, embs1: list,  df2: pd.DataFrame, embs2: list) -> float:
    answers1 = df1['chat_answer']
    answers2 = df2['chat_answer']
    sims = []
    max_count = min(len(answers1), len(answers2))
    for i in range(max_count):
        sims.append(float(util.cos_sim(embs1[i], embs2[i]).detach()))

    return sum(sims) / len(sims)

ps = [] 
for i, df in enumerate(dfs):
    p = get_performance(df, names[i])
    ps.append(p) 

generate_dashboard(ps)    
generate_similarity_matrix(ps, dfs)
for p in ps:
    generate_report(p)

