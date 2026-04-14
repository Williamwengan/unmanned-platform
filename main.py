import requests
import base64
import json
import sys
import os

# 配置 Ollama 服务的地址和端口
OLLAMA_URL = "http://localhost:40997/api/chat"
MODEL_NAME = "qwen3-vl:8b"


def encode_image_to_base64(image_path):
    """将图片文件转换为 base64 编码字符串"""
    if not os.path.exists(image_path):
        print(f"错误: 找不到图片文件 {image_path}")
        sys.exit(1)

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_scene(image_path):
    """调用 qwen3-vl 模型分析场景"""
    base64_image = encode_image_to_base64(image_path)

    # 核心：通过严格的 Prompt 限制模型只输出指定环境和物体，不要任何废话
    prompt = """
    仔细观察这张图片。
    任务1：识别图片场景属于以下哪一个环境：护理室、卧室、卫生间。
    任务2：列出环境中的可见物体。

    必须严格按照以下格式输出，绝对不要包含任何多余的解释、问候或其他信息：
    环境：[填入环境名称]
    物体：[填入物体列表，用逗号分隔]
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "images": [base64_image],
        "stream": False,
        "options": {
            "temperature": 0.1  # 调低温度，让模型输出更稳定、更少废话
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()  # 检查 HTTP 请求是否成功

        result = response.json()
        print(result.get("response", "模型没有返回任何内容"))

    except requests.exceptions.RequestException as e:
        print(f"请求 Ollama 服务失败: {e}")
        print("请检查 Ollama 是否已启动，以及端口 45295 是否正确。")


if __name__ == "__main__":
    # 使用示例：可以通过命令行传入图片路径，或者直接在这里修改
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        # 如果没有通过命令行传参，默认使用当前目录下的 test.jpg
        img_path = "test.png"

    print(f"正在分析图片: {img_path} ...\n")
    analyze_scene(img_path)