# 在页面上添加标题
import streamlit as st
import pandas as pd


st.set_page_config(
    layout="wide",  # 设置布局为宽屏
    initial_sidebar_state="expanded",
)
st.subheader("Configuration Search")

# 读取数据
df = pd.read_csv('configuration.csv')
df.drop('Label Name', axis=1, inplace=True)

with st.sidebar:
    min_value, max_value = st.slider(
                    "选择车型价格范围(万)",
                    min_value=int(df['官方指导价(万)'].min()),
                    max_value=int(df['官方指导价(万)'].max()),
                    value=(int(df['官方指导价(万)'].min()), int(df['官方指导价(万)'].max()))
                    )
    # 选择行和列
    # selected_model = st.selectbox("选择车型", df['车型'].unique())
    selected_config = st.selectbox("选择配置", df.columns.tolist()[4:], index=None, label_visibility="collapsed", placeholder="请选择配置" )

    if selected_config == None:
        selected_value = st.selectbox('选择配置值:', ['先选配置'], index=None, label_visibility="collapsed", placeholder="请选择配置值" )
    else:
        selected_value = st.selectbox('选择配置值:', df[selected_config].unique(), index=None, label_visibility="collapsed", placeholder="请选择配置值" )  
    button = st.button('确定')

data_show = st.empty()
if not button:
    with data_show.container():
        model_numbers = len(set(df['车型'].tolist()))
        st.caption(f"共{model_numbers}款车型，{len(df)}款配置")
        st.dataframe(df, height=800)
else:   
    # 查询原始数据
    filtered_df = df[(df['官方指导价(万)'] >= min_value) & (df['官方指导价(万)'] <= max_value)]
    # filtered_df = filter_df [(filter_df ['车型'] == selected_model) & (df[selected_config] == selected_value)]
    filtered_df = filtered_df[(df[selected_config] == selected_value)]
    # 显示查询结果
    data_show.empty()
    with data_show.container():
        model_numbers = len(set(filtered_df['车型'].tolist()))
        st.caption(f"查询结果：共{model_numbers}款车型，{len(filtered_df)}款配置")
        st.dataframe(filtered_df, height=800)
 