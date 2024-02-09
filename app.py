import openai
import streamlit as st

st.title("趣味旅行")
client = openai.OpenAI(api_key="https://api.openai.com/v1")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state["messages"] = []
prompt_placeholder = st.empty()
# 问卷封面部分
if "form_selected" not in st.session_state:
    st.session_state["form_selected"] = None
    prompt_placeholder.markdown("请选择你的旅行者身份开启副本")
cover_placeholder = st.empty()  # 创建一个新的占位符用于放置问卷封面按钮
# 创建一个新的占位符用于显示提示信息
if st.session_state["form_selected"] is None:
    cols = cover_placeholder.columns(3)  # 将问卷封面按钮放在新的占位符中
    with cols[0]:
        if st.button("问卷甲"):
            st.session_state["form_selected"] = "form1"
    with cols[1]:
        if st.button("问卷乙"):
            st.session_state["form_selected"] = "form2"
    with cols[2]:
        if st.button("问卷丙"):
            st.session_state["form_selected"] = "form3"
    if st.session_state["form_selected"] is not None:
        cover_placeholder.empty()  # 清空问卷封面按钮
        prompt_placeholder.empty()  # 清空提示信息
# 问卷部分
if st.session_state["form_selected"] is not None:
    form_placeholder = st.empty()
    skip_button_placeholder = st.empty()  # 创建一个新的占位符用于放置跳过按钮
    if "form_submitted" not in st.session_state or not st.session_state["form_submitted"]:
        with form_placeholder.form(key='my_form'):
            if st.session_state["form_selected"] == "form1":
                option1 = st.radio(
                    '您会选择以下哪种小众场景？',
                    ('A.美食刺客，越刺越勇', 'B.本地人都不知道的“世外桃源”', 'C.打卡绝美拍照点，争做网红创始人', 'D.其他(请填写)')
                )
                option2 = st.radio(
                    '您的旅游必备单品是？',
                    ('A.相机', 'B.墨镜', 'C.手电筒', 'D.各种速食食品', 'E.其他(请填写)')
                )
                option3 = st.radio(
                    '抵达目的地后，以下哪种情景会影响您的心情？',
                    ('A.景点没看头', 'B.找不到好吃的餐馆', 'C.手机突然没电', 'D.其他(请填写)')
                )
                option4 = st.radio(
                    '对您来说，本次旅途的目的是',
                    ('A.逃离城市，探索自然', 'B.促进感情，交换真心', 'C.探索未知，自由惬意', 'D.其他(请填写)')
                )
                option5 = st.radio(
                    '旅途结束以后，您会选择',
                    ('A.朋友圈分享本次旅程', 'B.记录旅行VLOG', 'C.编撰《XX的旅游日志》', 'D.其他(请填写)')
                )
            elif st.session_state["form_selected"] == "form2":
                option1 = st.radio(
                    '请您选择降落位置',
                    ('A.五岳', 'B.青藏高原', 'C.秦岭淮河一线', 'D.甘肃沙漠', 'E.岛屿孤勇者', 'F.其他(请填写)')
                )
                option2 = st.radio(
                    '请选择您的坐骑',
                    ('A.越野车', 'B.缆车', 'C.观光大巴', 'D.徒步最香', 'E.其他(请填写)')
                )
                option3 = st.radio(
                    '请选择挑战项目',
                    ('A.极限运动', 'B.山间野趣', 'C.洞穴奇案', 'D.勇闯“孤岛"', 'E.其他(请填写)')
                )
                option4 = st.radio(
                    '请选择您的驿站',
                    ('A.帐篷', 'B.房车', 'C.青年旅社', 'D.酒店', 'E.其他(请填写)')
                )
            else:
                option1 = st.radio(
                    '您偏好的躺平场景',
                    ('A.观光度假村', 'B.日落海滩', 'C.主题民宿大床房', 'D.农家乐', 'E.其他(请填写)')
                )
                option2 = st.radio(
                    '您偏好的项目',
                    ('A.足浴按摩', 'B.室内剧本杀', 'C.美容美发', 'D.寺庙祈福', 'E，采茶、摘果子', 'F.其他(请填写)')
                )
                option3 = st.radio(
                    '您偏好的酒店/度假村类型',
                    ('A.山间小舍', 'B.最炫民族风', 'C.网红民宿', 'D.海景房', 'E.其他(请填写)')
                )
                option4 = st.radio(
                    '如果让您来纪念本次旅途，您会选择',
                    ('A.特产', 'B.各种美食调料包', 'C.深度游，体验当地', 'D.主题游，专注兴趣')
                )
                option5 = st.radio(
                    '您的旅行预算是多少？',
                    ('A.不限，只要有趣', 'B.适中，性价比高', 'C.文创', 'D.照片', 'E.其他(请填写)')
                )
            submit_button = st.form_submit_button(label='提交')
        skip_button = skip_button_placeholder.button('填问卷太麻烦？一键开启盲盒旅行')
        # 如果用户提交了问卷，将问卷结果作为聊天机器人的输入
        if submit_button or skip_button:
            st.session_state["form_submitted"] = True
            form_placeholder.empty()  # 清除问卷
            skip_button_placeholder.empty()  # 清除跳过按钮
            st.markdown("欢迎咨询旅游服务")  # 显示欢迎消息
            if submit_button:
                status_message = st.empty()  # 创建状态消息的占位符
                status_message.write("正在为您生成旅游计划...")  # 显示状态消息
                full_response = ""
                for response in client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[{"role": "user",
                                   "content": f"我选择了：\n问题 1: {option1}\n问题 2: {option2}\n问题 3: {option3}\n问题 4: {option4}\n问题 5: {option5}"}],
                        stream=True,
                ):
                    full_response += (response.choices[0].delta.content or "")
                status_message.empty()  # 清除状态消息
                st.session_state.messages.append({"role": "assistant", "content": full_response})

# 在使用messages之前，检查它是否已经在session_state中初始化
if "messages" not in st.session_state:
    st.session_state["messages"] = []
# 聊天部分
if "form_submitted" in st.session_state and st.session_state["form_submitted"]:
    # 添加重置按钮
    if st.button('重置'):
        st.session_state.clear()
        st.experimental_rerun()  # 重定向到一个新的页面
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
        for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.get("messages", [])],
                stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
