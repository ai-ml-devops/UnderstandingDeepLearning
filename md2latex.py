import re
import os

def convert_markdown_to_latex(md_text):
    # 转换一级标题，去掉序号
    latex_text = re.sub(r'^# \d+(\.\d+)*\s*(.+)', r'\\chapter{\2}', md_text, flags=re.MULTILINE)
    
    # 转换二级标题，去掉序号
    latex_text = re.sub(r'^## \d+(\.\d+)*\s*(.+)', r'\\section{\2}', latex_text, flags=re.MULTILINE)
    
    # 转换三级标题，去掉序号
    latex_text = re.sub(r'^### \d+(\.\d+)*\s*(.+)', r'\\subsection{\2}', latex_text, flags=re.MULTILINE)
    
    # 转换行内公式
    latex_text = re.sub(r'(?<!\\)\$(.+?)\$', r'\\(\1\\)', latex_text)
    
    # 转换单行公式，保留align环境
    def replace_math(match):
        content = match.group(1)
        if '\\begin{align}' in content or '\\end{align}' in content:
            return f"{content}"
        else:
            return f"\\[{content}\\]"
    
    latex_text = re.sub(r'(?<!\\)\$\$(.+?)\$\$', replace_math, latex_text, flags=re.DOTALL)
    
    # 转换加粗文本
    latex_text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', latex_text)
    
    # 转换图片，并将 figures 替换为 png，将 svg 后缀替换为 png
    latex_text = re.sub(r'!\[([^\]]*)\]\(figures/([^)]+)\.svg\)', r'\\begin{figure}[h!]\n\\centering\n\\includegraphics[width=0.7\\linewidth]{png/\2.png}\n\\caption{\1}\n\\end{figure}', latex_text)
    
    return latex_text


def list_files():
    fs = []
    # 遍历目录及其子目录下的所有文件
    for root, dirs, files in os.walk('./'):
        if root.startswith('./.git') or root.startswith('./figures') or root.startswith('./latex'):
            continue
        for file in files:
            if not '.md' in file :
                continue
            if file == 'README.md':
                continue
            fs.append(file)
    return fs

fs = list_files()
for f in fs:
    if f in ['Chapter 1 Introduction.md', 'Chapter 2 Supervised learning.md', 'Chapter 3 Shallow neural networks.md']:
        continue
    print(f)
    num = re.search(r'Chapter (\d+)', f).group(1)
    if int(num) < 10:
        num = '0' + num
    tex_name = 'chapter' + num + '.tex'
    
    with open(f, 'r') as m:
        md_text = m.read()
    latex_text = convert_markdown_to_latex(md_text)
    with open(tex_name, "w") as f:
        f.write(latex_text)