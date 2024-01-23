## 9-16/01/2023

First experiments aimed at exploring the use of agent and tools. In these first experiments, all tool descriptions are integrated into the prompt using LangChain functions, and we force the agent to look at the description only, without letting him invoke them.

- [tools](tools) folder contains the specification of the tools. They are implemented either with the decorator <code>@tool</code> or by extending the <code>BaseTool</code> class.
- [agent_chain.py](agent_chain.py): it make usage of the LCEL sintax of LangChain. Here the input and the output is customized. The used agent is defined by ourself, not using one available from LangChain. We asked the Agent to generate (i) the process model in mermaid, (ii) the data flow, (iii) a python function to simulate the process.
- [agent_function.py](agent_function.py): it make usage of the LCEL sintax of LangChain. Here the experiments leverage on the potential usage of the function calling property of OpenAI.
- [agent_memory.py](agent_memory.py): this agent leverages on memory. Its prompt clearly separate two possibilities either (i) to generate the process model, the data flow and the pseudocode, or (ii) to simulate the process. If the user input a process description, the agent will goes for the (i) type of output by essentially looking at the tool documentation present in the prompt. If the user asks to simulate the process, the agent start invoking the tools based on the pseudocode previously generated. When the agent invoke the tools it has no control over loops and conditions. It is not able to see the output of the tools and the decision to be make.
- [agent.py](agent.py): this agent outputs the process model, the data flow and the pseudocode.

## Notes

With agents and tools, we can call the tools, but we cannot really simulate the process if we have loops or conditions. So I can create a Python script and run it.

We are inspired by agents and tools, where the agent uses a tool to answer a question from the user. In our case, we use tools as apis that implement some tasks of my process and ask the llm to identify the tasks of a process and identify from the tools those that allow me to execute them.

- The agent has no control over loops and conditions → generate a script and then execute it.
- Tools are used to enrich the model, they are used to respond to user input.
- Tools need to be well described and documented → can we use an LLM for this?
- Prompt length is limited, we need to include only the tools/APIs that can be useful (not all of them) in the prompt.