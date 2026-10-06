# my-react-agent

纯Python手写ReAct Agent，不依赖LangChain。

## 功能

- 手写ReAct循环（Thought → Action → Observation）
- 接入智谱GLM-4
- 支持多轮工具调用
- 工具：搜索（mock）、计算器
- 三层JSON容错（直接解析 → 清洗Markdown → 正则提取）

## 在线演示

https://my-react-agent-nnqugx3fujxhet6ep4rv5t.streamlit.app/

## 本地运行

pip install -r requirements.txt
streamlit run ui.py

## 项目结构

my_react_agent.py - Agent主循环
llm.py - LLM调用封装
ui.py - Streamlit界面
requirements.txt - 依赖

## 踩坑记录

- GLM-4返回的JSON带Markdown包裹，json.loads无法直接解析，加了三层容错
- finish时GLM-4把action_input填成null，改了system_prompt明确要求