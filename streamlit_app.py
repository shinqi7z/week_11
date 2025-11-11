import streamlit as st
import openai
import os

# 页面配置
st.set_page_config(
    page_title="Role-based Creative Chatbot",
    page_icon="🎭",
    layout="centered"
)

# 标题和描述
st.title("🎭 Role-based Creative Chatbot")
st.markdown("Select a creative role and ask your question!")

# API密钥输入
st.sidebar.header("API & Role Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

# 角色定义
roles = {
    "Video Director": {
        "description": "You are a professional film director. Always analyze ideas in terms of visual storytelling — use camera movement, lighting, framing, and emotional tone to explain your thoughts. Describe concepts as if you are planning a film scene.",
        "example": "How can I shoot a dream sequence?"
    },
    "Dance Instructor": {
        "description": "You are an experienced dance instructor. Focus on movement, rhythm, body expression, and emotional conveyance through dance. Provide practical advice on techniques and artistic expression.",
        "example": "How can I express sadness through movement?"
    },
    "Fashion Stylist": {
        "description": "You are a professional fashion stylist. Discuss color trends, materials, silhouettes, and personal style. Consider body types, occasions, and personality when giving advice.",
        "example": "What style fits a confident personality?"
    },
    "Acting Coach": {
        "description": "You are a seasoned acting coach. Teach emotion delivery, scene breakdown, character development, and natural expression. Focus on authenticity and technique.",
        "example": "How to express fear naturally on stage?"
    },
    "Art Curator": {
        "description": "You are an art curator with deep knowledge of art history and interpretation. Analyze artworks, compositions, emotional impact, and connect artistic choices with broader contexts.",
        "example": "How does this composition convey emotion?"
    }
}

# 角色选择
selected_role = st.sidebar.selectbox("Choose a role:", list(roles.keys()))

# 显示角色描述
st.sidebar.markdown(f"**Role Description:**")
st.sidebar.info(roles[selected_role]["description"])

# 主界面 - 问题输入
st.subheader(f"Ask the {selected_role}")
question = st.text_area(
    "Enter your question or idea:",
    placeholder=f"e.g., {roles[selected_role]['example']}",
    height=100
)

# 生成响应按钮
if st.button("Generate Response", type="primary"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        try:
            # 设置OpenAI API
            openai.api_key = api_key
            
            # 创建角色特定的系统提示
            system_prompt = roles[selected_role]["description"]
            
            # 调用OpenAI API
            with st.spinner(f"Consulting with {selected_role}..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
            
            # 显示响应
            st.subheader("Response:")
            st.success(response.choices[0].message.content)
            
        except openai.error.AuthenticationError:
            st.error("Invalid API key. Please check your OpenAI API key.")
        except openai.error.RateLimitError:
            st.error("Rate limit exceeded. Please try again later.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# 页脚
st.markdown("---")
st.markdown("**Built for Art & Advanced Big Data** - Prof. Jahwan Koo (SKKU)")

# 使用说明
with st.expander("How to use this chatbot"):
    st.markdown("""
    1. **Enter your OpenAI API key** in the sidebar
    2. **Select a creative role** from the dropdown
    3. **Ask a question** related to the chosen role
    4. **Click 'Generate Response'** to get professional advice
    
    **Available Roles:**
    - 🎬 **Video Director**: Film and video production expertise
    - 💃 **Dance Instructor**: Movement and expression guidance  
    - 👗 **Fashion Stylist**: Style and trend advice
    - 🎭 **Acting Coach**: Performance and emotion techniques
    - 🖼️ **Art Curator**: Art interpretation and analysis
    """)
