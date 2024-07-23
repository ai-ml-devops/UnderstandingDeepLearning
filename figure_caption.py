import streamlit as st

def parse(latex_text: str):
    # 分割文本
    parts = latex_text.split(r'\begin{figure}[h!]')


    # 处理分割后的文本，跳过第一个因为它在第一个figure之前
    new_parts = [parts[0]]
    for i in range(1, len(parts)):
        figure_block = r'\begin{figure}[h!]' + parts[i]
        figure_lines = figure_block.split('\n')
        figure_lines = [item for item in figure_lines if item]

        # 找到caption所在的行并替换内容
        for j in range(len(figure_lines)):
            if figure_lines[j].strip().startswith(r'\caption'):
                # 找到figure后的第一个段落
                caption_text = figure_lines[-1].strip()
                figure_lines[j] = r'\caption{' + caption_text + '}'
                break
        figure_lines = figure_lines[:-1]
        new_parts.append('\n'.join(figure_lines))

    # 合并文本
    new_latex_text = '\n\n'.join(new_parts)
    return new_latex_text


st.title('LaTeX Parser')

# 两个文本框布局
col1, col2 = st.columns(2)

with col1:
    st.header('输入')
    input_text = st.text_area("输入 LaTeX 文本", height=400)

with col2:
    st.header('输出')
    if input_text:
        output_text = parse(input_text)
        st.text_area("输出 LaTeX 文本", value=output_text, height=400)