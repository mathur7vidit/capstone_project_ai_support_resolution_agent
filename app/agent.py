import time

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

from langchain.agents import create_agent

from langchain_core.messages import HumanMessage

from app.tools import (
    ticket_status,
    escalate_case
)

from app.rag import retriever

from app.prompts import SYSTEM_PROMPT

from app.safety import (
    is_unsafe,
    mask_pii,
    requires_escalation
)

from app.logger import logging


# -----------------------------
# LLM
# -----------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# -----------------------------
# Tools
# -----------------------------

tools = [
    ticket_status,
    escalate_case
]


# -----------------------------
# Agent
# -----------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


# -----------------------------
# Main Function
# -----------------------------

def run_agent(query: str):

    total_start = time.time()

    logging.info(f"Incoming Query: {mask_pii(query)}")

    try:

        # -------------------------
        # Safety Check
        # -------------------------

        if is_unsafe(query):

            logging.warning("Unsafe request blocked")

            total_latency = time.time() - total_start

            return {
                "response": "Request refused due to safety policy.",
                "latency": round(total_latency, 2)
            }

        # -------------------------
        # Escalation Check
        # -------------------------

        if requires_escalation(query):

            escalation = escalate_case.invoke({
                "issue": query
            })

            logging.info("Case escalated")

            total_latency = time.time() - total_start

            return {
                "response": escalation,
                "latency": round(total_latency, 2)
            }

        # -------------------------
        # Retrieval Timing
        # -------------------------

        retrieval_start = time.time()

        docs = retriever.invoke(query)

        retrieval_latency = time.time() - retrieval_start

        logging.info(
            f"Retrieval latency: {retrieval_latency:.2f} sec"
        )

        retrieved_context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        # -------------------------
        # Final Prompt
        # -------------------------

        final_input = f"""
        User Question:
        {query}

        Retrieved Context:
        {retrieved_context}

        Instructions:
        - Use retrieved context only
        - Do not hallucinate
        - If information missing, say so
        """

        # -------------------------
        # LLM Timing
        # -------------------------

        llm_start = time.time()

        response = agent.invoke({
            "messages": [
                HumanMessage(content=final_input)
            ]
        })

        llm_latency = time.time() - llm_start

        logging.info(
            f"LLM latency: {llm_latency:.2f} sec"
        )

        # -------------------------
        # Extract Final Response
        # -------------------------

        final_response = response["messages"][-1].content

        total_latency = time.time() - total_start

        logging.info(
            f"Total latency: {total_latency:.2f} sec"
        )

        return {
            "response": final_response,
            "latency": round(total_latency, 2)
        }

    except Exception:

        logging.exception("Agent execution failed")

        total_latency = time.time() - total_start

        return {
            "response": "The support agent could not complete the request. Please try again shortly.",
            "latency": round(total_latency, 2)
        }
