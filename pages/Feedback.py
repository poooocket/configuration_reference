import streamlit as st
import pandas as pd
from datetime import datetime

# 在侧边栏创建一个表单
with st.form(key='feedback_form'):
    feedback = st.text_area("Share your feedback:")
    submit_button = st.form_submit_button(label='Submit')

# 处理反馈提交
if submit_button and feedback:
    # 尝试读取现有的反馈数据
    try:
        feedback_data = pd.read_csv('feedback.csv')
    except FileNotFoundError:
        # 如果文件不存在，创建一个新的DataFrame
        feedback_data = pd.DataFrame(columns=['Timestamp', 'Feedback'])

    # 确保 feedback_data 是一个DataFrame
    if isinstance(feedback_data, pd.DataFrame):
        # 添加新的反馈
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_feedback = pd.DataFrame([[current_time, feedback]], columns=['Timestamp', 'Feedback'])
        feedback_data = pd.concat([feedback_data, new_feedback], ignore_index=True)

        # 将数据保存到CSV文件
        feedback_data.to_csv('feedback.csv', index=False)
        st.success("Thank you for your feedback!")
    else:
        st.error("An error occurred while processing the feedback.")
