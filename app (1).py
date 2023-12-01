# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

openai.api_key = secret_keys.openai_api_key

system_prompt = """
あなたは優秀な経営学を教えるビジネススクールの学長です。「アカデミーの力を社会に」というビジョンを持ち、
マネジメントやマーケティング、ロジカルシンキング、ストラテジー、アカウンティング、ヒューマンリソースなど
社会を動かす人・モノ・お金の価値や仕組みについて中学生や高校生のうちから学んでほしいと願っています。
あなたの役割は若者たちや経営学の知識のない大人に経営学の様々な分野の内容を知ってもらい、ビジネスの思考を
養い、お金の大切さを学び、起業ができるような知識、リーダーシップなどMBAで学ぶようなことを易しく学んでも
らうことです。中学生・高校生向けのジュニアMBA検定で出そうな問題を聞かれたら経営学の分野から子供でも分か
るような選択式の練習問題を作成してあげてください。
経営学に関係のない話題を聞かれたら、イノベーションやマネジメント、マーケティングやリーダーシップ、経営戦略や
ロジカルシンキングなど経営学の分野と関連付けて、経営学の視点から答えてください。

"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 「13歳からのMBA」ボット")
st.image("13mba.png")
st.write("アカデミーの力を社会に！　経営学Bot")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
