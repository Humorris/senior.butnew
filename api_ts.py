from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
try:
    # 測試連線（這不花錢，只是檢查 API 是否通暢）
    models = client.models.list()
    print("OpenAI 連線成功！")
except Exception as e:
    print(f"OpenAI 連線失敗：{e}")
