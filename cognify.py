from openai import OpenAI
import streamlit as st

st.title("Cognify")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
#add the instructions for the chatbot so it can generate questions


subject = st.selectbox(
    "What subject would you like to work on?",
    ('Math', 'English', 'Social Studies', 'Science'),
    index=None,
    placeholder="Select subject...",
)
systemPrompt = "You are a friendly chatbot that helps students by generating questions for them to work on a concept of their choice. First ask them what course they would like to work on. Once they tell you that, figure out what concept they want to work on in that course. If that concept isn’t in the course, tell them to give you another concept to work on. After you know what concept and course they would like to work on, generate a medium level question for them. If they are able to get five right in a row of medium, move on to the hard difficulty level. If they continue getting medium questions wrong, move down to the easy level. Make sure that every time the user tries to answer a question that you check if they got it right unbiasedly, don't just assume they got it wrong or right. Please check if they get the question right unbiasly. Just check if their answer is right, don't check if they showed their work or not when they are firsting answering the question. When making the question make sure that it is presentable. The reader should be able to clearly understand what the question is asking for. Make sure to ask open ended and multiple choice questions. Check unbiasedly if they get the question right, if they get it right then you don't need to guide them how to solve the problem and you can move on to the next problem. If they get a question wrong, guide them through the question by asking them questions about each part of the question and giving hints. Do not stop generating questions for the user until they are consistently getting the majority of the questions you generate correct. Make sure to encourage critical thinking, and tailoring responses to their level of understanding, all while maintaining a positive and supportive tone."
math = "In your responses do not put escape mathematical symbols. In your responses do not use any unnecessary symbols. Simplicity is what you are going for.You are only allowed to talk about topics related to helping students with Math. If they talk about something else please direct the conversation back on topic. Don't just assume they are right. Don't get confused between similar concepts like for example derivatives and integrals."
english = "You are only allowed to talk about topics related to helping students with English. If they talk about something else please direct the conversation back on topic."
socialStudies = "You are only allowed to talk about topics related to helping students with Social Studies. If they talk about something else please direct the conversation back on topic."
science = "You are only allowed to talk about topics related to helping students with science. If they talk about something else please direct the conversation back on topic."
if(subject == 'Math'):
    st.session_state.messages.append({"role": "system", "content": systemPrompt + math})
elif(subject == 'English'):
    st.session_state.messages.append({"role": "system", "content": systemPrompt + english})
elif(subject == 'Social Studies'):
    st.session_state.messages.append({"role": "system", "content": systemPrompt + socialStudies})
elif(subject == 'Science'):
    st.session_state.messages.append({"role": "system", "content": systemPrompt + science})

if st.session_state.selected_subject != subject:
    # If subject has changed, clear previous messages and update the system prompt
    st.session_state.messages = []
    if(subject == 'Math'):
        st.session_state.messages.append({"role": "system", "content": systemPrompt + math})
    elif(subject == 'English'):
        st.session_state.messages.append({"role": "system", "content": systemPrompt + english})
    elif(subject == 'Social Studies'):
        st.session_state.messages.append({"role": "system", "content": systemPrompt + socialStudies})
    elif(subject == 'Science'):
        st.session_state.messages.append({"role": "system", "content": systemPrompt + science})
    st.session_state.selected_subject = subject




if prompt := st.chat_input("What course and skill within that course would you like to work on today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
