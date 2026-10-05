import json
from llm import call_llm
import re
# 模拟LLM：根据输入返回固定的Thought+Action
def mock_llm(prompt):
    if "Observation" in prompt:
        return json.dumps({
            "thought": "我已经拿到搜索结果了，可以回答用户",
            "action": "finish",
            "action_input": "北京今天晴，25度"
        })
    if "北京" in prompt:
        return json.dumps({
            "thought": "用户问北京天气，我需要调用搜索工具",
            "action": "search",
            "action_input": "北京天气"
        })
    return json.dumps({
        "thought": "我已经知道答案了",
        "action": "finish",
        "action_input": "你好，我是ReAct Agent"
    })


# 模拟工具
def search(query):
    return f"{query}：晴，30度"

#增加计算器工具
def calculator(expression):
    try:
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{e}"





# ReAct主循环
def run_agent(user_input, max_steps=5):
    history = f"用户问题：{user_input}\n"
    for step in range(max_steps):
        print(f"\n--- 第{step + 1}轮 ---")

        system_prompt = """你是一个ReAct Agent。根据用户问题和历史记录，决定下一步动作。
        你必须返回JSON格式，包含四个字段：
        - thought: 你的思考过程
        - action: 要么是"search"（调用搜索），要么是"calculator"（调用计算器），要么是"finish"（结束）
        - action_input: 如果是search，填搜索关键词；如果是calculator，填数学表达式；如果是finish，必须填给用户的最终答案，不要填null
        可用工具：
        - search: 搜索信息
        - calculator: 计算数学表达式，输入是Python表达式，比如 "25*1.8+32"
        注意：finish时action_input绝对不能为空，必须包含最终答案。
        只返回JSON，不要加任何其他文字。"""
        full_prompt = system_prompt + "\n\n" + history
        llm_output = call_llm(full_prompt)

        print(f"LLM输出：{llm_output}")

        #增加三层容错
        def parse_llm_output(llm_output):
            # 第一层：直接解析
            try:
                return json.loads(llm_output)
            except json.JSONDecodeError:
                pass

            # 第二层：清洗Markdown后解析
            try:
                cleaned = llm_output.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("```")[1]
                    if cleaned.startswith("json"):
                        cleaned = cleaned[4:]
                cleaned = cleaned.strip()
                return json.loads(cleaned)
            except (json.JSONDecodeError, IndexError):
                pass

            # 第三层：正则提取 {...} 后解析
            try:
                match = re.search(r'\{.*\}', llm_output, re.DOTALL)
                if match:
                    return json.loads(match.group())
            except json.JSONDecodeError:
                pass

            # 三层都失败
            return None

        parsed = parse_llm_output(llm_output)
        if parsed is None:
            print("解析失败，让LLM重新生成")
            history += "解析失败，请重新返回合法的JSON格式\n"
            continue

        thought = parsed["thought"]
        action = parsed["action"]
        action_input = parsed["action_input"]

        print(f"Thought：{thought}")
        print(f"Action：{action}({action_input})")

        if action == "finish":
            print(f"\n最终回答：{action_input}")
            return action_input

        ## 根据模型返回的action，决定执行哪个工具
        if action == "search":
            observation = search(action_input)
        elif action == "calculator":
            observation = calculator(action_input)
        else:
            observation = f"未知工具：{action}"


        print(f"Observation：{observation}")
        history += f"Observation：{observation}\n"

    print("\n达到最大步数，停止")
    return None


if __name__ == "__main__":
    run_agent("北京今天多少度？如果超过25度，帮我算一下华氏度")