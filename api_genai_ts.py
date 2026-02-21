from google import genai
import os

# 1. 檢查 Key 是否讀取成功
api_key = os.environ.get('GEMINI_API_KEY')
print(f"Gemini Key 讀取狀態: {'成功' if api_key else '失敗'}")

# 2. 初始化 Client
client = genai.Client(api_key=api_key)

try:
    print("正在測試連線至 Google Gemini...")
    # 簡單發送一個測試請求
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="Hi"
    )
    print("Gemini 連線成功！")
    print(f"AI 回覆內容: {response.text}")
except Exception as e:
    print("\n--- Gemini 錯誤詳細資訊 ---")
    print(f"錯誤類型: {type(e).__name__}")
    print(f"詳細訊息: {e}")
    # 檢查是否為版本問題或認證問題
