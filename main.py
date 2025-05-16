import streamlit as st
from PIL import Image
import google.generativeai as genai
import io


# 퍼스널 컬러 추천 데이터
facecolor_data = {
    '봄 웜톤': {
        '의상': ['라이트 옐로우', '코랄', '라이트 베이지', '연두색'],
        '화장법': ['코랄 립', '피치 블러셔', '골드 아이섀도우'],
        '코디': '밝고 화사한 파스텔 계열 원피스와 가벼운 메이크업으로 생기있는 느낌을 연출하세요.'
    },
    '여름 쿨톤': {
        '의상': ['라이트 블루', '라벤더', '쿨 핑크', '민트'],
        '화장법': ['로지 핑크 립', '쿨톤 블러셔', '실버 펄 아이섀도우'],
        '코디': '시원한 느낌의 연청 데님 자켓과 화이트 티셔츠, 핑크 립 포인트로 청량함을 강조해보세요.'
    },
    '가을 웜톤': {
        '의상': ['카멜', '올리브', '버건디', '머스타드'],
        '화장법': ['브릭 립', '브라운 블러셔', '카키/브론즈 아이섀도우'],
        '코디': '딥한 브라운 자켓과 올리브 컬러 스커트, 브릭 립으로 분위기 있는 가을룩을 완성하세요.'
    },
    '겨울 쿨톤': {
        '의상': ['블랙', '네이비', '와인', '로얄 블루'],
        '화장법': ['레드 립', '플럼 블러셔', '그레이 아이섀도우'],
        '코디': '세련된 블랙 수트와 레드 립으로 도시적인 매력을 뽐내보세요.'
    }
}

# Gemini Vision API를 활용한 퍼스널 컬러 분석 함수
def analyze_personal_color_gemini(image, gemini_api_key):
    import google.generativeai as genai
    import io

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro-vision')

    # 이미지를 바이너리로 변환
    buf = io.BytesIO()
    image.save(buf, format='JPEG')
    byte_data = buf.getvalue()

    prompt = (
        "이 인물의 퍼스널 컬러(봄 웜톤, 여름 쿨톤, 가을 웜톤, 겨울 쿨톤 중 하나)를 전문가처럼 진단해주고, 한글로 결과만 간단히 알려주세요."
    )

    try:
        response = model.generate_content(
            [
                prompt,
                {
                    "mime_type": "image/jpeg",
                    "data": byte_data,
                }
            ]
        )
        result = response.text.strip()
        return result
    except Exception as e:
        return f"Gemini API 오류: {e}"
# --- Streamlit 앱 UI ---
st.title("사진 업로드 기반 퍼스널 컬러 분석 및 코디 추천 (Google Gemini)")

gemini_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

if not gemini_api_key:
    st.info("Gemini API Key를 입력하세요.")
elif uploaded_file is None:
    st.info("사진을 업로드하세요.")
else:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption='업로드한 사진', use_column_width=True)
        st.write("Gemini Vision으로 퍼스널 컬러 분석 중...")

        personal_color = analyze_personal_color_gemini(image, gemini_api_key)
        st.success(f"분석 결과: {personal_color}")

        # 결과가 facecolor_data에 있을 때만 추천 정보 표시
        result_key = None
        for key in facecolor_data:
            if key in personal_color:
                result_key = key
                break

        if result_key:
            st.subheader(f"추천 의상 색상 🎨")
            st.write(", ".join(facecolor_data[result_key]['의상']))

            st.subheader("추천 화장법 💄")
            st.write(", ".join(facecolor_data[result_key]['화장법']))

            st.subheader("최종 코디 제안 👗")
            st.write(facecolor_data[result_key]['코디'])
        else:
            st.info("분석 결과가 예상한 퍼스널 컬러(봄 웜톤, 여름 쿨톤, 가을 웜톤, 겨울 쿨톤) 중 하나가 아닙니다. 답변: " + personal_color)
    except Exception as e:
        st.error(f"이미지 처리 중 오류가 발생했습니다: {e}")

st.write("---")
st.write("※ Gemini API Vision 요금이 부과되며, API Key는 외부에 노출되지 않도록 주의하세요.")
