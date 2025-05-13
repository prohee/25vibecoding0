import streamlit as st
# MBTI 유형에 따른 이모지와 추천 직업
mbti_data = {
    "INTJ": {
        "emoji": "🧠",
        "jobs": ["데이터 과학자", "소프트웨어 개발자", "전략 컨설턴트"]
    },
    "INFP": {
        "emoji": "🎨",
        "jobs": ["작가", "그래픽 디자이너", "심리 상담사"]
    },
    "ENTP": {
        "emoji": "💡",
        "jobs": ["기업가", "마케팅 전문가", "변호사"]
    },
    "ESFJ": {
        "emoji": "🤝",
        "jobs": ["교사", "인사 관리자", "간호사"]
    },
    # 여기에 다른 MBTI 유형을 추가하세요
}

# Streamlit 앱 설정
st.title('MBTI에 따른 추천 직업 및 이모지')

# 사용자 입력
mbti_type = st.selectbox(
    '당신의 MBTI 유형을 선택하세요:',
    mbti_data.keys()
)

# 선택된 MBTI 유형에 대한 정보 표시
if mbti_type:
    st.write(f"### 당신의 MBTI 유형: {mbti_type} {mbti_data[mbti_type]['emoji']}")
    st.write("#### 추천 직업:")
    for job in mbti_data[mbti_type]['jobs']:
        st.write(f"- {job}")

