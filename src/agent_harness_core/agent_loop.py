from agent_harness_core.llm import _build_llm
from agent_harness_core.tools import TOOLS,run_bash
from agent_harness_core.llm import MODEL
from agent_harness_core.prompt import SYSTEM

client=_build_llm()
def agent_loop(messages: list):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        # Append assistant turn
        messages.append({"role": "assistant", "content": response.content})
        # If the model didn't call a tool, we're done
        if response.stop_reason != "tool_use":
            return
        # Execute each tool call, collect results
        results = []
        for block in response.content:
            if block.type == "tool_use":
                # 输出调用
                print(f"\033[33m$ {block.input['command']}\033[0m")
                # 输出调用结果
                output = run_bash(block.input["command"])
                print(output[:200])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        # Feed tool results back, loop continues
        messages.append({"role": "user", "content": results})