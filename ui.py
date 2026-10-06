import streamlit as st
from my_react_agent import run_agent

st.title("ReAct Agent 演示")

user_input = st.text_input("输入你的问题：", "北京今天多少度？如果超过25度，帮我算一下华氏度")

if st.button("运行"):
    steps = run_agent(user_input)

    st.subheader("执行过程")
    for s in steps:
        st.write(f"**第{s['step']}步**")
        st.write(f"Thought: {s['thought']}")
        st.write(f"Action: {s['action']}({s['action_input']})")
        if "observation" in s:
            st.write(f"Observation: {s['observation']}")
        st.write("---")

    st.subheader("最终回答")
    st.write(steps[-1].get("final_answer", "未完成"))