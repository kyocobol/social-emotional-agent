import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from agent.graph import build_agent
from workflow.graph import build_workflow

st.title("Social-Emotional Agent")

if "agent" not in st.session_state:
    st.session_state.agent = build_agent()
    st.session_state.workflow = build_workflow()
    st.session_state.messages = []
    st.session_state.last_response = None
    st.session_state.conversation_ended = False
    st.session_state.analysis_report = None

with st.sidebar:
    st.header("Suicide Risk Detection")
    if last_response := st.session_state.last_response:
        colors = {"none": "🟢", "low": "🟡", "medium": "🟠", "high": "🔴"}
        st.metric(
            "Suicidal Ideation Level",
            f"{colors.get(last_response.suicidal_ideation_level, '⚪')} "
            f"{last_response.suicidal_ideation_level.capitalize()}",
        )
        st.metric(
            "Depression Level",
            f"{colors.get(last_response.depression_level, '⚪')} "
            f"{last_response.depression_level.capitalize()}",
        )
        st.divider()
        st.subheader("Risk Factors")
        st.checkbox(
            "Previous Suicide Attempt",
            value=last_response.previous_suicide_attempt,
            disabled=True,
        )
        st.checkbox(
            "Specific Suicide Plan",
            value=last_response.has_specific_suicide_plan,
            disabled=True,
        )
        st.checkbox(
            "Recent Severe Stress",
            value=last_response.recent_severe_stress_event,
            disabled=True,
        )
        st.checkbox(
            "Family/Friend Suicide History",
            value=last_response.family_or_friend_suicide_history,
            disabled=True,
        )
    else:
        st.info("Start a conversation to see risk factors.")

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    st.chat_message(role).write(msg.content)

if not st.session_state.conversation_ended:
    if user_input := st.chat_input("Message"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.chat_message("user").write(user_input)

        result = st.session_state.agent.invoke(
            {"messages": st.session_state.messages[:-1], "user_input": user_input}
        )

        last_response = result["last_response"]
        st.chat_message("assistant").write(last_response.message)
        st.session_state.messages.append(AIMessage(content=last_response.message))
        st.session_state.last_response = last_response
        st.session_state.conversation_ended = not last_response.should_continue
        st.rerun()


@st.dialog("Analysis Report", width="large")
def show_analysis_report():
    if not st.session_state.analysis_report:
        with st.spinner("Generating..."):
            result = st.session_state.workflow.invoke(
                {"messages": st.session_state.messages}
            )
            st.session_state.analysis_report = result["analysis_report"]
        st.rerun()

    st.markdown(st.session_state.analysis_report)

    if st.button("New Conversation"):
        st.session_state.messages = []
        st.session_state.last_response = None
        st.session_state.conversation_ended = False
        st.session_state.analysis_report = None
        st.rerun()


if st.session_state.conversation_ended:
    show_analysis_report()
