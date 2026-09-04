import os
import re

from google import genai
from rag.retriever import retrieve

from agent.memory import (
    ShortTermMemory,
    save_memory,
    load_memories
)

from tools.tools import (
    search_policy,
    get_employee_info,
    get_leave_balance
)


# Gemini client
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


class OfficeAssistant:

    def __init__(self):

        # Short-term memory
        self.short_term_memory = ShortTermMemory()

        # Long-term memory
        self.long_term_memory = load_memories()

    def decide_tool(self, question):

        """
        Decide which tool should handle the question.
        """

        question_lower = question.lower()

        # Leave-related questions
        if any(word in question_lower for word in [
            "leave",
            "casual leave",
            "earned leave",
            "sick leave"
        ]):
            return "leave"

        # Employee-related questions
        if any(word in question_lower for word in [
            "employee",
            "department",
            "designation",
            "joining date",
            "location",
            "who is"
        ]):
            return "employee"

        # Policy-related questions
        if any(word in question_lower for word in [
            "policy",
            "travel",
            "hotel",
            "reimbursement",
            "expense",
            "work from home",
            "leave policy",
            "benefits",
            "security"
        ]):
            return "policy"

        return "general"

    def run_tool(self, tool_name, question):

        """
        Execute the selected tool.
        """

        if tool_name == "policy":

            return search_policy(question)

        elif tool_name == "employee":

            employee_id = self.get_employee_id_from_context(question)

            if employee_id:
                return get_employee_info(employee_id)

            return "Please provide the employee ID."

        elif tool_name == "leave":

            employee_id = self.get_employee_id_from_context(question)

            if employee_id:
                return get_leave_balance(employee_id)

            return "Please provide the employee ID."

        return None

    def extract_employee_id(self, question):

        """
        Extract employee ID such as EMP001 from the question.
        """

        match = re.search(
            r"\bEMP\d+\b",
            question.upper()
        )

        if match:
            return match.group()

        return None

    def get_employee_id_from_context(self, question):

        """
        Get employee ID from the current question
        or from recent conversation history.
        """

        # First check the current question
        employee_id = self.extract_employee_id(question)

        if employee_id:
            return employee_id

        # If not found, check short-term memory
        messages = self.short_term_memory.get_messages()

        for message in reversed(messages):

            employee_id = self.extract_employee_id(
                message["content"]
            )

            if employee_id:
                return employee_id

        return None

    def detect_memory(self, question):

        """
        Detect whether the user wants to save
        something as long-term memory.
        """

        question_lower = question.lower()

        memory_phrases = [
            "remember that",
            "remember this",
            "keep in mind",
            "save this",
            "note that"
        ]

        for phrase in memory_phrases:

            if phrase in question_lower:

                # Find the position in the original question
                start_index = question_lower.find(phrase)

                # Extract information while preserving
                # original capitalization
                information = question[
                    start_index + len(phrase):
                ].strip()

                if information:

                    memory_item = {
                        "type": "user_preference",
                        "information": information
                    }

                    save_memory(memory_item)

                    # Keep in-memory copy updated
                    self.long_term_memory.append(
                        memory_item
                    )

                    return memory_item

        return None

    def build_context(self):

        """
        Build conversation context from short-term memory.
        """

        messages = self.short_term_memory.get_messages()

        if not messages:
            return ""

        context = ""

        for message in messages:

            context += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        return context

    def build_memory_context(self):

        """
        Build context from long-term memory.
        """

        if not self.long_term_memory:
            return ""

        context = ""

        for memory in self.long_term_memory:

            context += (
                f"Type: {memory.get('type', 'unknown')}\n"
                f"Information: "
                f"{memory.get('information', '')}\n"
            )

        return context

    def answer(self, question):

        """
        Main agent workflow.
        """

        # Save user question in short-term memory
        self.short_term_memory.add_message(
            "user",
            question
        )

        # Check if the user wants to save something
        memory_item = self.detect_memory(question)

        # Build long-term memory context
        memory_context = self.build_memory_context()

        # Decide which tool to use
        tool_name = self.decide_tool(question)

        # Execute tool
        tool_result = self.run_tool(
            tool_name,
            question
        )

        # Build conversation context
        conversation = self.build_context()

        if tool_result:

            prompt = f"""
You are an intelligent Office Assistant for
Novatrix Technologies.

Answer the user's question using the information
provided by the selected company tool.

Do not invent information.

Conversation history:
{conversation}

Long-term memory:
{memory_context}

Tool used:
{tool_name}

Tool result:
{tool_result}

User question:
{question}

Give a concise and helpful answer.
"""

        else:

            prompt = f"""
You are an intelligent Office Assistant for
Novatrix Technologies.

Answer the user's question naturally.

Use the conversation history and long-term memory
when useful.

Do not invent company-specific information.

Conversation history:
{conversation}

Long-term memory:
{memory_context}

User question:
{question}

Give a concise and helpful answer.
"""

        # Generate final answer
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        answer = response.text

        # Add citations for policy answers
        if tool_name == "policy":

            results = retrieve(
                question,
                top_k=3
            )

            sources = []

            for result in results:

                citation = (
                    f"{result['source']}, "
                    f"Page {result['page']}"
                )

                if citation not in sources:
                    sources.append(citation)

            if sources:

                answer += "\n\nSources:\n"

                for source in sources:

                    answer += (
                        f"- {source}\n"
                    )

        # If memory was saved, acknowledge it
        if memory_item:

            answer = (
                "I've saved that to long-term memory.\n\n"
                + answer
            )

        # Store assistant response in short-term memory
        self.short_term_memory.add_message(
            "assistant",
            answer
        )

        return answer


if __name__ == "__main__":

    assistant = OfficeAssistant()

    print("\nOffice Assistant")
    print("----------------")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = assistant.answer(question)

        print("\nAssistant:", answer)
        print()