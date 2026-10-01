import json


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
    return f"{query}：晴，25度"


# ReAct主循环
def run_agent(user_input, max_steps=5):
    history = f"用户问题：{user_input}\n"
    for step in range(max_steps):
        print(f"\n--- 第{step + 1}轮 ---")
        llm_output = mock_llm(history)
        print(f"LLM输出：{llm_output}")

        parsed = json.loads(llm_output)
        thought = parsed["thought"]
        action = parsed["action"]
        action_input = parsed["action_input"]

        print(f"Thought：{thought}")
        print(f"Action：{action}({action_input})")

        if action == "finish":
            print(f"\n最终回答：{action_input}")
            return action_input

        observation = search(action_input)
        print(f"Observation：{observation}")
        history += f"Observation：{observation}\n"

    print("\n达到最大步数，停止")
    return None


if __name__ == "__main__":
    run_agent("北京天气怎么样")