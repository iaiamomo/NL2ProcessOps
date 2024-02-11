import pandas as pd
from ProcessGenLLM import ToolDict

def get_tools(all_tools, tools):
    res_tools = {}
    for tool in tools:
        for tool_elem in all_tools:
            tool_key = list(tool_elem.keys())[0]
            if tool_elem[tool_key]["description"] in tool:
                if res_tools == {}:
                    res_tools = tool_elem
                else:
                    res_tools.update(tool_elem)
    print(res_tools)
    return res_tools


def main():
    all_tools = ToolDict().tools

    df = pd.read_csv('processes.csv')

    data = []
    # for each row in the dataframe
    for _, row in df.iterrows():
        tools = row['input']
        tools = tools.split('\n')
        res_tools = get_tools(all_tools, tools)
        process = row['output']
        data.append([res_tools, process])

    res_df = pd.DataFrame(data, columns=['tools', 'process'])
    print(res_df)
    res_df.to_csv('processes_tools.csv', sep=',', index=False)


if __name__ == "__main__":
    main()