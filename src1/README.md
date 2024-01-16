## 9-16/01/2023

First experiments aiming at a first exploration of the usage of Agent and Tools. In this first experiments all the tools descriptions are integrated in the prompt by using LangChain functions and we force the agent only to look at the description without letting him invoking them.

- [tools](tools) folder contains the specification of the tools. They are implemented either with the decorator <code>@tool</code> or by extending the <code>BaseTool</code> class.
- [agent_chain.py](agent_chain.py): it make usage of the LCEL sintax of LangChain. Here the input and the output is customized. The used agent is defined by ourself, not using one available from LangChain. We asked the Agent to generate (i) the process model in mermaid, (ii) the data flow, (iii) a python function to simulate the process.
- [agent_function.py](agent_function.py): it make usage of the LCEL sintax of LangChain. Here the experiments leverage on the potential usage of the function calling property of OpenAI.
- [agent_memory.py](agent_memory.py): this agent leverages on memory. Its prompt clearly separate two possibilities either (i) to generate the process model, the data flow and the pseudocode, or (ii) to simulate the process. If the user input a process description, the agent will goes for the (i) type of output by essentially looking at the tool documentation present in the prompt. If the user asks to simulate the process, the agent start invoking the tools based on the pseudocode previously generated. When the agent invoke the tools it has no control over loops and conditions. It is not able to look at the output of the tools and the decision to take.
- [agent.py](agent.py): this agent output the process model, the data flow and te pseudocode.

## Notes

With agents and tools, we are able to invoke the tools but we are not able to really simulate the process in case we have loops or conditions. I can therefore create a python script and execute it.

We take inspiration from the agents and tools, where the agent use a tool to answer a question of the user. In our case, we use tools as apis implementing some tasks of my process and ask the llm to identify the tasks of a process and identify from the tools those that let me execute it.

- agent does not have control over loops and conditions → generate a script and then execute it
- tools are used to enrich the model, they are used to answer to the user input
- tools need to be well described and documented → can we use an llm to do so?
- prompt length is limited, we need to include in the prompt only the tools/apis that can be useful (not all of them).