import streamlit as st
from PIL import Image
import os
import base64

# -------------------------- 基础配置 --------------------------
TARGET_MONTH = 4
TARGET_DAY = 22
IMAGE_FOLDER = "images"
MUSIC_FILE = "bgm.mp3"

TIME_DATA = {
    "2023": ["06月", "07月", "08月", "09月", "10月", "11月", "12月"],
    "2024": ["01月", "02月", "03月", "04月", "06月", "07月"],
    "2025": ["02月", "04月", "05月", "06月", "07月", "08月", "09月", "10月", "11月"],
    "2026": ["02月", "04月", "05月"]
}

# -------------------------- 音乐转码函数 --------------------------
def get_audio_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -------------------------- 页面样式设置 --------------------------
st.set_page_config(page_title="我们的纪念相册", layout="wide")
st.markdown("""
<style>
.main {
    background-color: #fff8f8;
}
.stSelectbox, .stButton, .stMarkdown {
    font-size: 18px;
}
.love-text {
    font-family: serif;
    color: #b84b4b;
    text-align: center;
    font-size: 20px;
    margin: 10px 0 20px;
}
.book-box {
    border: 2px solid #e8c8c8;
    border-radius: 12px;
    padding: 20px;
    background-color: #fff5f5;
}
</style>
""", unsafe_allow_html=True)

# -------------------------- 解锁逻辑 + 恋爱文案 --------------------------
st.title("💌 专属恋爱纪念相册")
st.markdown('<div class="love-text">「以日期为密，赴一场岁岁年年的约」</div>', unsafe_allow_html=True)
st.subheader("请输入我们的专属纪念日，解锁专属回忆")

col1, col2 = st.columns(2)
with col1:
    select_month = st.selectbox("月份", list(range(1, 13)), index=0)
with col2:
    select_day = st.selectbox("日期", list(range(1, 32)), index=0)

unlock_success = False
if select_month == TARGET_MONTH and select_day == TARGET_DAY:
    unlock_success = True
    st.balloons()
    st.markdown('<div class="love-text">解锁成功✨ 从此朝暮与年岁并往，我们与爱意同行</div>', unsafe_allow_html=True)

    # 背景音乐，点击页面触发
    audio_b64 = get_audio_base64(MUSIC_FILE)
    audio_html = f"""
    <audio id="bgm" loop>
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    <script>
        document.addEventListener('click', function() {{
            const audio = document.getElementById('bgm');
            audio.play().catch(e => console.log("播放触发：",e));
        }}, {{once: true}});
    </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# -------------------------- 书页翻页式相册 --------------------------
if unlock_success:
    st.divider()
    st.header("📖 回忆手账 · 书页翻页")

    selected_year = st.selectbox("选择年份", list(TIME_DATA.keys()))
    selected_month = st.selectbox("选择月份", TIME_DATA[selected_year])

    pic_path = os.path.join(IMAGE_FOLDER, selected_year, selected_month)
    pic_list = []
    if os.path.exists(pic_path):
        all_files = os.listdir(pic_path)
        pic_list = [f for f in all_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        pic_list.sort()

    if not pic_list:
        st.warning("当前月份的书页还没有故事哦，敬请期待～")
    else:
        # 翻页状态保存
        if "page_idx" not in st.session_state:
            st.session_state.page_idx = 0

        total_page = len(pic_list)
        current_idx = st.session_state.page_idx

        # 书页容器
        st.markdown('<div class="book-box">', unsafe_allow_html=True)
        pic_full_path = os.path.join(pic_path, pic_list[current_idx])
        img = Image.open(pic_full_path)
        st.image(img, use_column_width=True, caption=f"第 {current_idx + 1} 页 / 共 {total_page} 页")
        st.markdown('</div>', unsafe_allow_html=True)

        # 上一页 / 下一页 按钮
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("◀ 上一页") and current_idx > 0:
                st.session_state.page_idx -= 1
        with col_next:
            if st.button("下一页 ▶") and current_idx < total_page - 1:
                st.session_state.page_idx += 1