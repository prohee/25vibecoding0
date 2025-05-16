import streamlit as st
from PIL import Image

# ... (facecolor_data 등은 위 코드와 동일)

st.title("사진 업로드 기반 퍼스널 컬러 분석 및 코디 추천 (OpenAI Vision)")

openai_api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and openai_api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드한 사진', use_column_width=True)
    st.write("OpenAI Vision으로 퍼스널 컬러 분석 중...")

    # OpenAI API로 분석
    personal_color = analyze_personal_color_api(image, openai_api_key)
    st.success(f"분석 결과: {personal_color}")

    # 결과가 facecolor_data에 있으면 추천, 아니면 안내
    if personal_color in facecolor_data:
        st.subheader(f"추천 의상 색상 🎨")
        st.write(", ".join(facecolor_data[personal_color]['의상']))

        st.subheader("추천 화장법 💄")
        st.write(", ".join(facecolor_data[personal_color]['화장법']))

        st.subheader("최종 코디 제안 👗")
        st.write(facecolor_data[personal_color]['코디'])
    else:
        st.info("분석 결과가 예상한 퍼스널 컬러(봄 웜톤, 여름 쿨톤, 가을 웜톤, 겨울 쿨톤) 중 하나가 아닙니다. 답변: " + personal_color)

elif not openai_api_key:
    st.info("OpenAI API Key를 입력해주세요.")
else:
    st.info("사진을 업로드하면 자동으로 퍼스널 컬러 분석이 시작됩니다.")
