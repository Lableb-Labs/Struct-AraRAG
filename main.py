import pandas as pd

from llm_factory.LLMSpecialists import LLMSpecialists
from process.router_pipline import HybridRetrieverSystem
from data_preprocessing.normalization import arabic_normalization

df = pd.read_csv("dataset/AraAggBench_100_Questions_TestSet.csv")
questions = df["Question_Arabic"]

def run_struct_rag_pipline(question):
    question = arabic_normalization(question)
    answer = None
    results =  HybridRetrieverSystem().process_query(question)
    contents = results["results"]
    if results["route"]  ==  "VECTOR" or results["route"] == "HYBRID":
        if len(contents) > 0:
            passage = '\n Book Content: '.join([c["text"] for c in contents])
            answer = LLMSpecialists().question_answering(question, passage)
    elif results["route"] == "SQL":
        answer = results["results"]

    else:
        answer = results["results"]
    return answer


for question in questions:
    answer = run_struct_rag_pipline(question)
    print("question : ", question  , " -  answer : ", answer)
    print("-------------------------\n\n")
