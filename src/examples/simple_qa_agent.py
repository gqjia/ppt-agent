#!/usr/bin/env python3
"""
简单的问答 Agent 示例，使用 smolagents 框架
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from smolagents.agents import ToolCallingAgent, PromptTemplates, PlanningPromptTemplate, FinalAnswerPromptTemplate, ManagedAgentPromptTemplate
from smolagents.models import OpenAIModel

class SimpleQAAgent:
    """简单的问答 Agent，专注于回答 Python 编程问题"""
    
    def __init__(self):
        # 创建模型
        model = OpenAIModel("gpt-4o-mini")
        
        # 创建完整的提示模板
        planning_prompt = PlanningPromptTemplate(
            initial_plan="请根据以下要求制定一个详细的计划来回答问题：{question}",
            update_plan_pre_messages="根据之前的计划和当前进展，更新计划：{current_plan}",
            update_plan_post_messages="基于最新信息更新计划：{current_plan}"
        )
        final_answer_prompt = FinalAnswerPromptTemplate(
            answer="这是最终答案：{answer}",
            pre_messages="在提供最终答案之前：{context}",
            post_messages="最终答案之后：{follow_up}"
        )
        managed_agent_prompt = ManagedAgentPromptTemplate(
            instruction="请执行以下指令：{instruction}",
            task="请完成以下任务：{task}",
            report="任务报告：{report}"
        )
        
        prompt_templates = PromptTemplates(
            system_prompt=self._get_system_prompt(),
            planning=planning_prompt,
            final_answer=final_answer_prompt,
            managed_agent=managed_agent_prompt
        )
        
        self.agent = ToolCallingAgent(
            tools=[],
            model=model,
            prompt_templates=prompt_templates
        )
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """
        你是一个专业的 Python 编程专家，负责回答与 Python 相关的问题。
        
        你的主要职责：
        1. 提供准确的 Python 编程知识
        2. 解释复杂的概念以易于理解的方式
        3. 提供代码示例（如果适用）
        4. 确保答案简洁明了
        
        请专注于 Python 编程问题，并提供有帮助且准确的回答。
        """
    
    def ask_question(self, question: str) -> str:
        """向 agent 提问
        
        Args:
            question: 用户的问题
            
        Returns:
            agent 的回答
        """
        try:
            question_prompt = f"""
            请回答以下关于 Python 编程的问题：
            
            {question}
            
            请提供清晰、简洁且准确的回答。如果适用，请包含代码示例。
            """
            response = self.agent.run(question_prompt)
            return response
        except Exception as e:
            return f"回答问题时出错: {str(e)}"

def create_simple_qa_agent() -> SimpleQAAgent:
    """创建简单问答 agent 实例"""
    return SimpleQAAgent()

if __name__ == "__main__":
    # 测试简单问答 agent
    qa_agent = create_simple_qa_agent()
    
    # 提出一些关于 Python 的问题
    questions = [
        "如何在 Python 中创建一个列表推导式？",
        "什么是 Python 中的装饰器，它是如何工作的？",
        "如何在 Python 中处理文件读取和写入？"
    ]
    
    for q in questions:
        print(f"\n问题: {q}")
        print("回答:")
        answer = qa_agent.ask_question(q)
        print(answer) 