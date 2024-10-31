__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

def create_intent_classification_crew():
    """Create CrewAI crew for intent classification"""
    intent_classifier = Agent(
        role='Intent Classifier',
        goal='Accurately classify user queries as either CET course-related or industrial partnership-related or general-question',
        backstory="""You are an expert in understanding user intentions and classifying queries.
        You have deep knowledge of both educational courses and industrial partnerships.""",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    )
    
    def classify_intent(query: str) -> str:
        classification_task = Task(
            description=f"""Analyze the following query and classify it as either 'adult_learner' 
            (for CET course-related queries) or 'industrial_partner' (for partnership-related queries).
            
            Query: {query}
            
            Consider:
            - If the query mentions courses, training, learning, or skills development, it's likely 'adult_learner'
            - If the query mentions collaboration, partnership, industry projects, or business opportunities, 
              it's likely 'industrial_partner'
            - Else it is 'general question'
            
            Return ONLY 'adult_learner' or 'industrial_partner' or 'general question' as your answer.""",

            expected_output="""
            Return ONLY 'adult_learner' or 'industrial_partner' or 'general question' as your answer.""",

            agent=intent_classifier
        )
        
        crew = Crew(
            agents=[intent_classifier],
            tasks=[classification_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result.raw.strip()
    
    return classify_intent