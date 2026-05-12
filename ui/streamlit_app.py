import os

import streamlit as st
import requests


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
FASTAPI_URL = f"{BACKEND_URL.rstrip('/')}/chat"
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "60"))


st.set_page_config(
    page_title="AI Support Resolution Agent",
    layout="centered"
)


st.title("AI Support Resolution Agent")

st.markdown(
    "Customer Support AI using LangChain + RAG"
)


query = st.text_input(
    "Ask your support question:"
)


if st.button("Submit"):

    if query.strip():

        with st.spinner("Generating response..."):

            try:

                response = requests.post(
                    FASTAPI_URL,
                    json={
                        "query": query
                    },
                    timeout=REQUEST_TIMEOUT_SECONDS
                )

                response.raise_for_status()

                result = response.json()

                st.subheader("Response")
                st.write(result.get("response", "No response returned."))

                st.subheader("Latency")

                if "latency" in result:
                    st.write(f"{result['latency']} sec")
                else:
                    st.write("Latency unavailable")

            except requests.Timeout:

                st.error("The backend took too long to respond. Please try again.")

            except requests.ConnectionError:

                st.error("The backend is unavailable. Please try again shortly.")

            except requests.HTTPError:

                st.error("The backend could not process the request. Please try again.")

            except Exception:

                st.error("Something went wrong. Please try again.")

    else:

        st.warning("Please enter a query.")
