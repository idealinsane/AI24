import streamlit as st
from openai import OpenAI

class TravelPlanner:
    def __init__(self):
        self.client = OpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1/",
        )
        self.model = "deepseek-r1:1.5b"

    def process_request(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )
            result = st.empty()
            collected_chunks = []

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    collected_chunks.append(chunk.choices[0].delta.content)
                    result.markdown("".join(collected_chunks))

            return "".join(collected_chunks)

        except Exception as e:
            return f"Error: {str(e)}"

def get_system_prompts():
    return {
        "Trip Itinerary": '''You are a travel expert who creates detailed and personalized trip itineraries.\nFollow these guidelines:\n1. Start with an overview of the destination\n2. Include a day-by-day breakdown of activities\n3. Suggest must-visit attractions and hidden gems\n4. Provide recommendations for local cuisine and dining\n5. Include transportation tips and options\n6. Add cultural or historical context for key locations\n7. Offer packing tips based on the destination's climate''',
        "Travel Tips": '''You are a seasoned traveler who provides practical advice for smooth trips.\nProvide tips on:\n1. Best times to visit specific destinations\n2. Budgeting and saving money while traveling\n3. Navigating local customs and etiquette\n4. Staying safe and healthy during travel\n5. Packing efficiently for different types of trips\n6. Finding affordable accommodations and flights\n7. Making the most of layovers and short trips''',
        "Destination Recommendations": '''You are a travel guide who suggests destinations based on user preferences.\nConsider:\n1. The traveler's interests (e.g., adventure, relaxation, culture)\n2. Budget constraints\n3. Preferred climate and season\n4. Travel duration\n5. Group size and demographics (e.g., family, solo, couple)\n6. Accessibility and travel restrictions\n7. Unique experiences or events happening at the destination''',
    }

def get_example_prompts():
    return {
        "Trip Itinerary": {
            "placeholder": '''Examples:\n1. "Plan a 5-day trip to Japan focusing on culture and food"\n2. "Create a 7-day itinerary for a family vacation in Italy"\n3. "Suggest a 3-day weekend getaway for adventure lovers in Costa Rica"\n4. "Design a 10-day road trip across the American Southwest"\n5. "Plan a romantic 4-day trip to Paris"\n\nYour request:''',
            "default": "Plan a 7-day trip to Japan focusing on culture and food",
        },
        "Travel Tips": {
            "placeholder": '''Ask for travel tips or advice.\nExamples:\n1. "What are the best ways to save money while traveling in Europe?"\n2. "How can I stay safe while traveling solo in South America?"\n3. "What should I pack for a two-week trip to Southeast Asia?"\n4. "What are some tips for traveling with young children?"\n5. "How do I handle language barriers in non-English-speaking countries?"''',
            "default": "What are the best ways to save money while traveling in Europe?",
        },
        "Destination Recommendations": {
            "placeholder": '''Describe your preferences for destination suggestions.\nExamples:\n1. "I want a relaxing beach vacation with good food and clear water"\n2. "I'm looking for an adventurous trip with hiking and wildlife"\n3. "Suggest a cultural destination with historical sites and museums"\n4. "I need a budget-friendly destination for a family of four"\n5. "Where can I go for a romantic getaway with stunning views?"''',
            "default": "I want a relaxing beach vacation with good food and clear water",
        },
    }

def main():
    st.set_page_config(
        page_title="DeepSeek R1 Travel Assistant", page_icon="✈️", layout="wide"
    )

    st.title("✈️ Local DeepSeek R1 Travel Assistant")
    st.markdown("### 학번 이름")
    st.markdown(
        """
Using DeepSeek R1 1.5B model running locally through Ollama
"""
    )

    system_prompts = get_system_prompts()
    example_prompts = get_example_prompts()

    # Sidebar
    st.sidebar.title("Settings")
    mode = st.sidebar.selectbox(
        "Choose Mode", ["Trip Itinerary", "Travel Tips", "Destination Recommendations"]
    )

    # Show current mode description
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Current Mode**: {mode}")
    st.sidebar.markdown("**Mode Description:**")
    st.sidebar.markdown(system_prompts[mode].replace("\n", "\n\n"))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### Input for {mode}")
        user_prompt = st.text_area(
            "Enter your travel preferences or questions:",
            height=300,
            placeholder=example_prompts[mode]["placeholder"],
            value=example_prompts[mode]["default"],
        )
        process_button = st.button(
            "✈️Process", type="primary", use_container_width=True
        )

    with col2:
        st.markdown("### Output")
        output_container = st.container()

    if process_button:
        if user_prompt:
            with st.spinner("Planning your trip..."):
                with output_container:
                    assistant = TravelPlanner()
                    assistant.process_request(system_prompts[mode], user_prompt)
        else:
            st.warning("⚠️ Please enter some input!")

if __name__ == "__main__":
    main()
