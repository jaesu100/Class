import random
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🎯 숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS 스타일링 (매력적이고 세련된 UI)
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1.05rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .welcome-card {
        background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%);
        border-radius: 12px;
        padding: 18px 22px;
        border-left: 5px solid #667eea;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    .result-card-up {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 15px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        margin: 15px 0;
    }
    .result-card-down {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 15px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        margin: 15px 0;
    }
    .result-card-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 20px;
        border-radius: 12px;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 4px 12px rgba(40,167,69,0.15);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# 3. 세션 상태 초기화 함수
def init_game_state(reset_best=False):
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []  # [(시도회수, 추측값, 결과), ...]
    st.session_state.feedback = None
    if reset_best or "best_score" not in st.session_state:
        st.session_state.best_score = None


# 최초 상태 초기화
if "secret_number" not in st.session_state:
    init_game_state()


# 4. 사이드바 구성
with st.sidebar:
    st.header("🏆 게임 상태 & 전적")
    
    # 최고 기록 표시
    best_score_display = (
        f"{st.session_state.best_score} 회" 
        if st.session_state.best_score is not None 
        else "기록 없음"
    )
    st.metric(label="🥇 최고 기록 (최소 시도)", value=best_score_display)
    st.metric(label="🔢 현재 시도 횟수", value=f"{st.session_state.attempts} 회")
    
    st.divider()
    
    st.subheader("⚙️ 게임 조작")
    if st.button("🔄 새 게임 시작", use_container_width=True, type="primary"):
        init_game_state()
        st.toast("새로운 비밀 숫자가 생성되었습니다! 🎲", icon="🎲")
        st.rerun()

    if st.button("🗑️ 최고 기록 초기화", use_container_width=True):
        st.session_state.best_score = None
        st.toast("최고 기록이 초기화되었습니다.", icon="🧹")
        st.rerun()

    with st.expander("📖 게임 규칙 보기"):
        st.write("""
        1. **범위**: 1부터 100 사이의 숫자를 맞춥니다.
        2. **목표**: 가능한 **최소 시도 횟수**로 성공하세요!
        3. **힌트**:
           - **UP!**: 정답이 입력값보다 더 큽니다.
           - **DOWN!**: 정답이 입력값보다 더 작습니다.
        """)


# 5. 메인 화면 웰컴 및 헤더
st.markdown('<div class="main-title">🎯 숫자 맞추기 게임</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">1부터 100 사이의 비밀 숫자를 최소 시도 횟수로 맞춰보세요!</div>', unsafe_allow_html=True)

# 웰컴 가이드 카드
st.markdown("""
<div class="welcome-card">
    <b>👋 환영합니다!</b><br>
    컴퓨터가 <b>1~100</b> 사이의 무작위 숫자를 하나 골랐습니다.<br>
    아래 입력창에 숫자를 입력하고 <b>[제출하기]</b> 버튼을 누르면 힌트가 제공됩니다.
</div>
""", unsafe_allow_html=True)


# 6. 게임 진행 로직
if not st.session_state.game_over:
    # 사용자 입력 폼
    with st.form(key="guess_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            user_guess = st.number_input(
                "숫자를 입력하세요 (1~100):",
                min_value=1,
                max_value=100,
                value=50,
                step=1,
                key="input_guess"
            )
        with col2:
            st.write("") # 수평 맞춤용 여백
            st.write("")
            submit_button = st.form_submit_button("🎯 제출하기", use_container_width=True)

    if submit_button:
        st.session_state.attempts += 1
        secret = st.session_state.secret_number

        if user_guess < secret:
            st.session_state.feedback = ("UP", f"📈 **UP!** ({user_guess}보다 더 큰 숫자입니다.)")
            st.session_state.history.append((st.session_state.attempts, user_guess, "📈 UP"))
        elif user_guess > secret:
            st.session_state.feedback = ("DOWN", f"📉 **DOWN!** ({user_guess}보다 더 작은 숫자입니다.)")
            st.session_state.history.append((st.session_state.attempts, user_guess, "📉 DOWN"))
        else:
            st.session_state.game_over = True
            st.session_state.feedback = ("SUCCESS", f"🎉 정답입니다! 비밀 숫자는 **{secret}** 이었습니다!")
            st.session_state.history.append((st.session_state.attempts, user_guess, "🎉 정답!"))
            
            # 최고 기록 업데이트
            if (st.session_state.best_score is None or 
                st.session_state.attempts < st.session_state.best_score):
                st.session_state.best_score = st.session_state.attempts
                st.toast("🏆 신기록 달성!", icon="🎉")

            st.balloons()
            st.rerun()

    # 피드백 출력 (UP / DOWN)
    if st.session_state.feedback:
        fb_type, fb_msg = st.session_state.feedback
        if fb_type == "UP":
            st.warning(fb_msg, icon="📈")
        elif fb_type == "DOWN":
            st.info(fb_msg, icon="📉")

else:
    # 게임 성공 완료 화면
    st.markdown(f"""
    <div class="result-card-success">
        🎉 축하합니다! 정답을 맞추셨습니다! 🎉<br><br>
        🎯 비밀 숫자: <b>{st.session_state.secret_number}</b><br>
        🏆 총 시도 횟수: <b>{st.session_state.attempts}회</b>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 다시 시도하기 (새 게임)", type="primary", use_container_width=True):
            init_game_state()
            st.rerun()
    with col_btn2:
        if st.button("🛑 게임 종료하기", use_container_width=True):
            st.success("게임을 플레이해주셔서 감사합니다! 언제든 다시 접속해주세요. 👋")


# 7. 시도 히스토리 타임라인 / 기록 표
if st.session_state.history:
    st.divider()
    st.subheader("📜 시도 기록")
    
    # 최근 시도가 상단에 오도록 역순 정리
    history_df = [
        {"시도": f"{h[0]}회차", "입력한 숫자": h[1], "결과": h[2]} 
        for h in reversed(st.session_state.history)
    ]
    st.dataframe(history_df, use_container_width=True)
