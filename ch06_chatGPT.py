import streamlit as st
import openai
import os
from datetime import datetime

#### 메인 함수 ####
def main():
    # 기본 설정
    st.set_page_config(
        page_title="chatGPT 텍스트 비서 서비스",
        layout="wide")
def STT(apikey):
    client = openai.OpenAI(api_key= apikey)
    
    # session stare 최기화
    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

def ask_gpt(prompt, modle, apikey):
    client = openai.OpenAI(api_key=apikey)
    response = client.chat.completions.create(
        model="",
        messages=prompt)
    gptResponse = response.choices[0].message.content

    
    # 제목
    st.header("chatGPT 텍스트 비서 서비스")

    # 구분선
    st.markdown("---")

    # 기본설명
    with st.expander("chatGPT 비서 서비스에 관하여", expanded=True):
        st.write(
        """
        - chatGPT 비서 프로그램은 UI 스트림릿을 활용했습니다.
        - STT(Speech-To-Text)는 OpenAI의 Whisper AI를 활용했습니다.
        - 답변은 OpenAI의 GPT 모델을 활영했습니다.
        - TTS(Text-To-Speech)는 구글의 Googel Translate TTS를 활용했습니다.
        """
        )

        st.markdown("")
    # 사이드 바 생성
    with st.sidebar:
        # open ai api 키 입력받기
        st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")

        st.markdown("---")

        # gpt모델을 선택하기 위한 라디오 버튼 생성
        model= st.radio(label="GPT 모델", options=["gpt-4", "gpt-3.5-turbo"])

        st.markdown("---")


        # 리셋 버튼 생성
        if st.button(label="초기화"):
            # 리셋 코드
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]
            st.session_state["check_reset"] = True
    
    # 기능 구현 공간
    col1, col2 = st.columns(2)
    with col1:
        # 왼쪽 영역 작성
        st.subheader("질문하기")
        now= datetime.now().strftime("%H:%M")
        st.session_state["chat"] = st.session_state["chat"]+[("user", now, question)]

        st.session_state["messages"] = st.session_state["messages"]+[{"role":"user", "content":question}]
    
    with col2:
        st.subheader("질문/답변")
        
        response = ask_gpt(st.session_state["messages"],modle,st.session_state["OPENAI_API"] )

        st.session_state["messages"] = st.session_state["messages"] + [{"role":"system", "content":response}]

        now= datetime.now().strftime("%H:%M")
        st.session_state["chat"] = st.session_state["chat"]+[("bot", now, response)]

        for sender, time, message in st.session_state["chat"]:
            if sender == "user":
                st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                st.write("")
            else:
                st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                st.write("")

if __name__=="__main__":
    main()