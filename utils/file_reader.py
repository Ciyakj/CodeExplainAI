
def read_code_files(uploaded_files):
    code_data = ""
    for file in uploaded_files:
        if file.name.endswith((".py", ".js", ".java", ".md", ".txt")):
            content = file.read().decode("utf-8", errors="ignore")
            code_data += f"\n# File: {file.name}\n{content}\n"
    return code_data
