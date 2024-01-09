import streamlit as st
import pandas as pd
from datetime import datetime

# 在侧边栏创建一个表单

with st.form(key='feedback_form'):
    feedback = st.text_area("Share your feedback:")
    submit_button = st.form_submit_button(label='Submit')

# 处理反馈提交
if submit_button and feedback:
    # 读取现有的反馈数据或创建一个新的空DataFrame
    try:
        feedback_data = pd.read_csv('feedback.csv')
    except FileNotFoundError:
        feedback_data = pd.DataFrame(columns=['Timestamp', 'Feedback'])

    # 添加新的反馈
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_feedback = {'Timestamp': current_time, 'Feedback': feedback}
    feedback_data = feedback_data.append(new_feedback, ignore_index=True)

    # 将数据保存到CSV文件
    feedback_data.to_csv('feedback.csv', index=False)
    st.success("Thank you for your feedback!")