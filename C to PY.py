import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="C-to-Python Converter", page_icon="🛡️")

# --- 사이드바: API 키 입력 ---
with st.sidebar:
    st.title("🔐 보안 설정")
    user_api_key = st.text_input(
        "OpenAI API Key를 입력하세요", 
        type="password", 
        help="입력하신 키는 서버에 저장되지 않고 브라우저 세션 동안만 사용됩니다."
    )
    st.info("API 키는 [OpenAI Dashboard](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.")

st.title("📂 C-to-Python AI 변환기")
st.write("나만의 API 키를 사용하여 안전하게 코드를 변환하세요.")

# --- 메인 화면 로직 ---
uploaded_file = st.file_uploader("C 언어 파일(.c)을 선택하세요", type=["c"])

if uploaded_file is not None:
    c_code = uploaded_file.read().decode("utf-8")
    
    if st.button("🚀 파이썬으로 변환하기"):
        # API 키 입력 여부 확인
        if not user_api_key:
            st.error("❌ 왼쪽 사이드바에서 API 키를 먼저 입력해주세요!")
        else:
            with st.spinner("AI가 코드를 분석 중입니다..."):
                try:
                    # 입력받은 키로 클라이언트 생성
                    client = OpenAI(api_key=user_api_key)
                    
                    prompt = f"""
                    당신은 C언어 코드를 실행 가능한 Python 코드로 완벽하게 변환하는 전문 에이전트입니다.

                    [C Code]
                    {c_code}

                    [변환 지침]
                    1. 순수 코드 출력: ```python 이나 ``` 같은 마크다운 태그를 절대 붙이지 마세요.
                    2. 실행 가능성: 변환된 코드는 추가 수정 없이 즉시 실행 가능해야 합니다.
                    3. 주석 처리: 모든 설명은 반드시 파이썬 주석(#)으로 코드 내부에 포함하세요.
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    py_code = response.choices[0].message.content
                    py_code = py_code.replace("```python", "").replace("```", "").strip()

                    st.success("✅ 변환 완료!")
                    st.code(py_code, language="python")

                    # 다운로드 기능
                    st.download_button(
                        label="📥 변환된 파일 다운로드",
                        data=py_code,
                        file_name=uploaded_file.name.replace(".c", ".py"),
                        mime="text/x-python"
                    )
                except Exception as e:
                    st.error(f"❌ 오류 발생: API 키가 올바른지 확인해주세요. (상세: {e})")