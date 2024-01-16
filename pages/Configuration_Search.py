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
# 获取配置列表
config_list = df.columns.tolist()[4:]

if 'price_range_2' not in st.session_state:
    st.session_state['price_range_2'] = (int(df['官方指导价(万)'].min()), int(df['官方指导价(万)'].max()))

if 'selected_config' not in st.session_state:
    st.session_state['selected_config'] = config_list[0]

if 'selected_value' not in st.session_state:
        st.session_state['selected_value'] = None

with st.sidebar:
    min_value, max_value = st.slider("选择车型价格范围(万)", min_value=int(df['官方指导价(万)'].min()), max_value=int(df['官方指导价(万)'].max()), value = st.session_state['price_range_2'])
    config_index = config_list.index(st.session_state['selected_config'])
    selected_config = st.selectbox("选择配置", config_list, index=config_index) 

    if selected_config:
        value_list = df[selected_config].unique().tolist()
        if st.session_state['selected_value'] == None:
            selected_value = st.selectbox('选择配置值:', value_list, index=None)
        else:
            value_index = value_list.index(st.session_state['selected_value'])
            selected_value = st.selectbox('选择配置值:', value_list, index=value_index) 
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
    st.session_state['price_range_2'] = (min_value, max_value)
    st.session_state['selected_config'] = selected_config 
    st.session_state['selected_value'] = selected_value 
