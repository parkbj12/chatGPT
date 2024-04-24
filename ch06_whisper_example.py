import openai

# 모델 생성 및 API 키 입력
API_KEY = "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"
client = openai.OpenAI(api_key = API_KEY)

transcript = client._transportions.create(model = "whisper-1")
# 결과보기
print(transcript.text)
