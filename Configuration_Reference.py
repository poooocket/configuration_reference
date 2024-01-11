import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import re
import pandas as pd

# 定义条件判断函数，根据数值大小替换成范围
def replace_with_range(value):
    if value < 10:
        return "<10"
    if 10 <= value < 15:
        return "10-15"
    elif 15 <= value < 20:
        return "15-20"
    elif 20 <= value < 25:
        return "20-25"
    elif 25 <= value < 30:
        return "25-30"
    elif 30 <= value < 35:
        return "30-35" 
    elif 35 <= value < 40:
        return "35-40" 
    else:
        return ">40"

# 定义一个函数，用于提取字符串中的数字部分
def extract_number(s):
    if pd.notnull(s):
        pattern = r'\d+'  # 正则表达式匹配一个或多个数字
        numbers = re.findall(pattern, s)
        if numbers:
            return int(numbers[0])  # 返回第一个匹配到的数字
    else:
        return None
    
def extract_model(text):
    """
    Extract the brand from a string by identifying the year and returning the text before it.
    Assumes the year is a four-digit number and part of a larger string.
    """
    import re

    # Find all four-digit numbers in the text
    match = re.search(r'\d{4}', text)
    if match:
        year_index = match.start()
        return text[:year_index].strip()
    return text

def model_count(df, column_name):
    model_list = []
    for configuration in df[column_name]:
        model = extract_model(configuration)
        model_list.append(model)
    return len(set(model_list))

# 在页面上添加标题
st.set_page_config(
    layout="wide",  # 设置布局为宽屏
    initial_sidebar_state="expanded",
)
st.subheader("Configuration Reference")

# 读取数据
df = pd.read_csv('configuration.csv')

# 重命名列名
rename_dict = {'官方指导价': '官方指导价(万)'}
df.rename(columns=rename_dict, inplace=True)

 # 基本清洗
df['官方指导价(万)'] = df['官方指导价(万)'].str.replace('万', '').astype(float)# 将价格数据由字符串转换为数值
df.fillna("None", inplace=True) # 填空
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x) # 去除空格
df = df.applymap(lambda x: re.sub(r'\s*图示$', '', x) if isinstance(x, str) and re.search(r'\s*图示$', x) else x) # 去除“图示”字符

 #处理字符数据
df['驾驶辅助影像'] = df['驾驶辅助影像'].replace({'': 'None', '●倒车影像图示 ●360°全景影像 ●透明影像': '●倒车影像 ●360°全景影像 ●透明影像', '●倒车影像  ●360°全景影像': '●倒车影像 ●360°全景影像'}, regex=False)
df['巡航系统'] = df['巡航系统'].replace({'': 'None', '●定速巡航图示 ●自适应巡航 ●全速自适应巡航': '●定速巡航 ●自适应巡航 ●全速自适应巡航'}, regex=False)
df['手机App远程控制'] = df['手机App远程控制'].replace({'●远程控制 ●充电管理 ●服务预约': '●充电管理 ●远程控制 ●服务预约',
                                        '●车辆监控 ●充电管理 ●服务预约 ●远程控制': '●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●远程控制 ●充电管理 ●服务预约 ●车辆监控': '●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●远程控制 ●车辆监控 ●充电管理 ●服务预约': '●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●数字钥匙 ●车辆监控 ●远程控制 ●充电管理 ●服务预约': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●车辆监控 ●远程控制 ●充电管理 ●服务预约 ●数字钥匙': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约', 
                                        '●数字钥匙 ●充电管理 ●远程控制 ●车辆监控 ●服务预约': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●数字钥匙 ●远程控制 ●充电管理 ●服务预约 ●车辆监控': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●数字钥匙 ●远程控制 ●服务预约 ●充电管理 ●车辆监控': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●数字钥匙 ●远程控制 ●车辆监控 ●充电管理 ●服务预约': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●车辆监控 ●远程控制 ●充电管理 ●服务预约 ○数字钥匙': '○数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●车辆监控 ●远程控制 ●数字钥匙 ●充电管理 ●服务预约': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●远程控制 ●数字钥匙 ●充电管理 ●服务预约 ●车辆监控': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约',
                                        '●车辆监控 ●充电管理 ●服务预约 ●远程控制 ●智能寻车助手': '●车辆监控 ●充电管理 ●远程控制 ●服务预约 ●智能寻车助手',
                                        '●车辆监控 ●充电管理 ●服务预约 ●远程控制 ●智能寻车助手 ●数字钥匙': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约 ●智能寻车助手',
                                        '●数字钥匙 ●车辆监控 ●远程控制 ●充电管理 ●服务预约 ●智能寻车助手': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约 ●智能寻车助手',
                                        '●数字钥匙 ●车辆监控 ●远程控制 ●服务预约 ●充电管理 ●智能寻车助手': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约 ●智能寻车助手',
                                        '●车辆监控 ●远程控制 ●充电管理 ●服务预约 ●数字钥匙 ●智能寻车助手': '●数字钥匙 ●车辆监控 ●充电管理 ●远程控制 ●服务预约 ●智能寻车助手'
                                        }, regex=False)

df['车载智能系统'] = df['车载智能系统'].replace({'●DiLink智能网联': '●DiLink智能网联系统'}, regex=False)
df['辅助驾驶操作系统'] = df['辅助驾驶操作系统'].replace({'': 'None', '●DiPilot智能辅助驾驶系统': '●DiPilot智能驾驶辅助系统'}, regex=False)
df['USB/Type-C最大充电功率'] = df['USB/Type-C最大充电功率'].replace({'': 'None'}, regex=False)
df['主动安全预警系统'] = df['主动安全预警系统'].replace({'': 'None', '●车道偏离预警 ●前方碰撞预警  ●倒车车侧预警 ●DOW开门预警': '●车道偏离预警 ●前方碰撞预警 ●倒车车侧预警 ●DOW开门预警'}, regex=False)
df['4G/5G网络'] = df['4G/5G网络'].replace({'': 'None'}, regex=False)
df['车载智能芯片'] = df['车载智能芯片'].replace({'': 'None'}, regex=False)
df['辅助驾驶芯片'] = df['辅助驾驶芯片'].replace({'': 'None'}, regex=False)
df['车载智能芯片'] = df['车载智能芯片'].replace({'●骁龙8155': '●高通骁龙8155',
                                        '●高通8155':'●高通骁龙8155',
                                        '●高通6125':'●高通骁龙6125',
                                        '●高通骁龙SA8155':'●高通骁龙8155'}, regex=False)
df['语音分区域唤醒识别功能'] = df['语音分区域唤醒识别功能'].replace({'': 'None'}, regex=False)
df['遥控钥匙类型'] = df['遥控钥匙类型'].replace({'○智能遥控钥匙 ●NFC/RFID钥匙 ●手机蓝牙钥匙': '○智能遥控钥匙 ●手机蓝牙钥匙 ●NFC/RFID钥匙', 
                                    '○智能遥控钥匙1200元 ●手机蓝牙钥匙 ●NFC/RFID钥匙': '○智能遥控钥匙 ●手机蓝牙钥匙 ●NFC/RFID钥匙',
                                    '●普通遥控钥匙  ●可穿戴钥匙': '●普通遥控钥匙 ●可穿戴钥匙',
                                    '●普通遥控钥匙  ●可穿戴钥匙 ●手机蓝牙钥匙': '●普通遥控钥匙 ●手机蓝牙钥匙 ●可穿戴钥匙',
                                    '●智能遥控钥匙   ○可穿戴钥匙': '●智能遥控钥匙 ○可穿戴钥匙',
                                    '●智能遥控钥匙 ●NFC/RFID钥匙 ●手机蓝牙钥匙 ●UWB数字钥匙': '●智能遥控钥匙 ●手机蓝牙钥匙 ●NFC/RFID钥匙 ●UWB数字钥匙',
                                    '●智能遥控钥匙 ●可穿戴钥匙 ●手机蓝牙钥匙': '●智能遥控钥匙 ●手机蓝牙钥匙 ●可穿戴钥匙',
                                    '●智能遥控钥匙 ●手机蓝牙钥匙  ○可穿戴钥匙': '●智能遥控钥匙 ●手机蓝牙钥匙 ○可穿戴钥匙 '}, regex=False)

# 处理雷达和摄像头数据，将字符串中的数字部分提取出来，然后转换为整数
df['超声波雷达数量(个)'] = df['超声波雷达数量(个)'].apply(extract_number)
df['毫米波雷达数量(个)'] = df['毫米波雷达数量(个)'].apply(extract_number)
df['车外摄像头数量(个)'] = df['车外摄像头数量(个)'].apply(extract_number)
df['车内摄像头数量(个)'] = df['车内摄像头数量(个)'].apply(extract_number)

# 配置分组
basic_info = ['厂商', '级别', '能源类型', '上市时间', '电动机', '纯电续航里程(km)工信部', '纯电续航里程(km)CLTC', '充电时间(小时)', '快充电量(%)', '最大功率(kW)', '最大扭矩(N·m)', '变速箱', '长x宽x高(mm)', '车身结构', '最高车速(km/h)', '官方百公里加速时间(s)', '百公里耗电量(kWh/100km)', '电能当量燃料消耗量(L/100km)', '等速续航里程(km)', '整车保修期限', '首任车主保修期限', '6万公里保养总成本预估']
vehicle_body = ['长(mm)', '宽(mm)', '高(mm)', '轴距(mm)', '前轮距(mm)', '后轮距(mm)', '车门数(个)', '车门开启方式', '座位数(个)', '整备质量(kg)', '满载质量(kg)', '行李舱容积(L)', '风阻系数(Cd)']
electric_motor = [ '电动机描述', '电机类型', '电动机总功率(kW)', '电动机总马力(Ps)', '电动机总扭矩(N·m)', '前电动机最大功率(kW)', '前电动机最大扭矩(N·m)', '后电动机最大功率(kW)', '后电动机最大扭矩(N·m)', '驱动电机数', '电机布局']
battery = ['电池类型', '电芯品牌', '电池组质保', '电池容量(kWh)', '电池能量密度(Wh/kg)', '电池充电', '最大快充功率(kw)', '快充接口位置', '慢充接口位置', '电池温度管理系统', '单踏板模式', '换电支持', '品牌自营充电站', 'VTOL移动电站功能']
transmission = ['变速箱描述', '挡位数', '变速箱类型']
chassis_steering = ['驱动方式', '四驱类型', '前悬挂形式', '后悬挂形式', '转向类型', '车体结构']
brake_system = ['前制动器类型', '后制动器类型', '驻车制动类型', '前轮胎规格尺寸', '后轮胎规格尺寸', '备胎规格']
active_safety = ['ABS防抱死', '制动力分配(EBD/CBC等)', '刹车辅助(EBA/BA等)', '牵引力控制(TCS/ASR等)', '车身稳定系统(ESP/DSC等)', '主动安全预警系统', '主动刹车', '并线辅助', '车道保持辅助系统', '车道居中保持', '疲劳驾驶提示', '主动式DMS疲劳检测', '车内生命体征检测', '道路交通标识识别', '信号灯识别', '夜视系统']
passive_safety = ['前排安全气囊', '侧安全气囊', '侧安全气帘', '前排膝部气囊', '中央安全气囊', '安全带未系提示', '胎压监测系统', '儿童座椅接口(ISOFIX)', '被动行人保护', '安全轮胎']
control_assistance = ['驻车雷达', '前车驶离提醒', '驾驶辅助影像', '巡航系统', '自动变道辅助', '匝道自动驶出（入）', '辅助驾驶级别', '自动泊车入位', '循迹倒车', '记忆泊车', '自动驻车(AUTOHOLD)', '上坡辅助(HAC)', '陡坡缓降(HDC)', '可变悬挂调节', '空气悬挂', '电磁感应悬挂', '可变转向比系统', '前桥限滑方式', '后桥限滑方式', '中央差速器锁止功能', '整体主动转向系统', '驾驶模式选择', '制动能量回收系统', '低速行车警示音']
external = ['天窗类型', '光感天幕', '车顶行李架', '运动外观套件', '电动扰流板', '主动闭合式进气格栅', '铝合金轮毂', '无框设计车门', '隐藏式门把手', '拖挂钩']
internal = ['方向盘材质', '方向盘调节', '方向盘电动调节', '方向盘功能', '行车电脑屏幕', '液晶仪表样式', '液晶仪表尺寸(英寸)', '液晶仪表分辨率', '液晶仪表屏幕像素密度（PPI）']
comfort = ['电动吸合门', '电动后尾门', '感应式后尾门', '电动后尾门位置记忆', '车内中控锁', '遥控钥匙类型', '无钥匙进入', '无钥匙启动', '远程启动', '遥控移动车辆', '车辆召唤功能', '抬头显示系统(HUD)', '内置行车记录仪', '原厂ETC', '主动降噪', '手机无线充电', '手机无线充电最大功率(W)', '110V/220V/230V电源插座', '行李舱12V电源接口']
seat = ['座椅材质', '座椅皮质风格', '运动风格座椅', '第二排独立座椅', '座椅电动调节', '主驾座椅整体调节', '主驾座椅局部调节', '副驾座椅整体调节', '副驾座椅局部调节', '第二排座椅整体调节', '第二排座椅局部调节', '前排座椅功能', '第二排座椅功能', '老板键', '前/后扶手', '后排杯架', '可加热/制冷杯架', '后排座椅放倒比例', '第二排小桌板']
connection = ['中控屏尺寸(英寸)', '中控台彩色屏幕分辨率', '中控台彩色屏幕像素密度（PPI）', '中控下屏幕尺寸(英寸)', '中控下屏幕分辨率', '中控下屏幕像素密度（PPI）', '副驾驶屏幕尺寸(英寸)', '副驾驶屏幕分辨率', '副驾驶屏幕像素密度（PPI）', '可旋转/移动中控屏', '触屏振动反馈', 'GPS导航系统', 'AR实景导航', '导航路况信息展示', '道路救援服务', '蓝牙/车载电话', '手机互联映射', '车联网', '4G/5G网络', 'OTA升级', 'OTA版本', '面部识别', '指纹识别', '声纹识别', '情绪识别', '语音识别控制系统', '语音免唤醒功能', '语音分区域唤醒识别功能', '连续性语音识别', '可见即可说', '语音助手唤醒词', '手势控制功能', 'Wi-Fi热点']
entertainment = ['多指飞屏操控', '应用商店', '多媒体接口', 'USB/Type-C接口数量', 'USB/Type-C最大充电功率', '车载电视', '后排液晶屏', '模拟声浪', 'K歌功能', '音响品牌', '扬声器数量(个)', '后排多媒体控制']
lighting = ['近光灯', '远光灯', '日间行车灯', '自适应远近光', '自动大灯', '转向辅助灯', '前雾灯', '大灯随动转向(AFS)', '大灯高度调节', '大灯清洗功能', '车内氛围灯', '主动式环境氛围灯', '灯光特色功能', '大灯延时关闭', '前大灯雨雾模式']
glass = ['电动车窗', '车窗一键升降', '车窗防夹手功能', '外后视镜功能', '内后视镜功能', '车内化妆镜', '后排隐私玻璃', '车内遮阳帘', '雨量感应式雨刷', '后雨刷', '多层隔音玻璃', '前风挡电加热', '可加热喷水嘴']
air_condition = ['空调控制方式', '后排独立空调', '后排出风口', '温度分区控制', '车载空气净化器', '车内PM2.5过滤装置', 'HEPA过滤装置', '负离子发生器', '车内香氛装置', '车载冰箱']
intelligent_configuration = ['辅助驾驶操作系统', '辅助驾驶芯片', '辅助驾驶芯片算力(TOPS)', '车载智能芯片', '车载智能系统', '车机系统内存(GB)', '车机系统存储(GB)', '手机App远程控制', '热泵管理系统', '车外摄像头数量(个)', '车外摄影头像素', '车内摄像头数量(个)', '车内摄影头像素', '超声波雷达数量(个)', '毫米波雷达数量(个)', '激光雷达数量(个)', '激光雷达品牌', '激光雷达线数(线)', '激光雷达点云数量(万/秒)', '亚米级高精定位系统', '高精度地图', '哨兵（千里眼）模式', 'V2X通讯']

dict = {'基本信息': basic_info, 
        '车身': vehicle_body,
        '电动机': electric_motor,
        '电池/充电': battery,
        '变速箱': transmission,
        '底盘/转向': chassis_steering,
        '车轮/制动': brake_system,
        '主动安全': active_safety, 
        '被动安全': passive_safety,
        '辅助/操控': control_assistance, 
        '外部配置': external,
        '内部配置': internal,
        '舒适/防盗': comfort, 
        '座椅配置': seat,
        '智能互联': connection, 
        '影音娱乐': entertainment, 
        '灯光配置': lighting,
        '玻璃/后视镜': glass,
        '空调/冰箱': air_condition,
        '智能化配置': intelligent_configuration
        }
keys_list = list(dict.keys())

data_show_placeholder = st.empty() 
with data_show_placeholder.container():
    model_list = model_count(df, 'Label Name')
    st.caption(f"共{model_list}款车型，{len(df)}款配置")
    st.dataframe(df, height=800)

with st.sidebar:
    with st.form("my_form"):
        # 创建一个滑块选择器，选择范围
        min_value, max_value = st.slider(
            "选择车型价格范围(万)",
            min_value=int(df['官方指导价(万)'].min()),
            max_value=int(df['官方指导价(万)'].max()),
            value=(int(df['官方指导价(万)'].min()), int(df['官方指导价(万)'].max()))
        )

        selected_keys = st.multiselect("选择参数配置", keys_list)
        submitted = st.form_submit_button("确定")

# 根据选择器筛选数据
if submitted:
    filter_df = df[(df['官方指导价(万)'] >= min_value) & (df['官方指导价(万)'] <= max_value)]
    

    data_show_placeholder.empty()
    with data_show_placeholder.container():
        if not selected_keys:
            model_list = model_count(df, 'Label Name')
            st.caption(f"共{model_list}款车型，{len(df)}款配置")
            st.dataframe(df)
        else:
            selected_columns = ['Label Name',  '官方指导价(万)']
            for key in selected_keys:
                for column_name in dict[key]:
                    selected_columns.append(column_name)
            model_list = model_count(filter_df, 'Label Name')
            st.caption(f"共{model_list}款车型，{len(filter_df)}款配置")
            st.dataframe(filter_df[selected_columns])    
        st.divider()  
        
        # 使用apply函数将数值根据条件判断替换成范围
        filter_df['官方指导价(万)'] = filter_df['官方指导价(万)'].apply(replace_with_range)
        for column_name in selected_columns[2:]:
            cross_tab = pd.crosstab(filter_df[column_name], filter_df['官方指导价(万)'])
            col1, col2 = st.columns(2)
            col1.dataframe(cross_tab)
            col2.bar_chart(cross_tab)
            st.divider()
