"""
Planner Agent - 负责将PPT生成任务拆分成多个子任务并分配给其他agent处理
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import json
from loguru import logger

from smolagents.agents import ToolCallingAgent, PromptTemplates, PlanningPromptTemplate, FinalAnswerPromptTemplate, ManagedAgentPromptTemplate
from smolagents.models import OpenAIModel


class TaskType(Enum):
    """任务类型枚举"""
    RESEARCH = "research"           # 资料收集
    CONTENT_WRITING = "content"     # 内容撰写
    SLIDE_DESIGN = "design"         # 幻灯片设计
    IMAGE_GENERATION = "image"      # 图片生成
    REVIEW_EDIT = "review"          # 审查编辑
    FINAL_ASSEMBLY = "assembly"     # 最终组装


@dataclass
class SubTask:
    """子任务数据结构"""
    id: str
    type: TaskType
    title: str
    description: str
    dependencies: List[str]  # 依赖的其他任务ID
    estimated_duration: int  # 预计完成时间（分钟）
    priority: int  # 优先级（1-5，1最高）
    assigned_agent: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None


@dataclass
class PPTProject:
    """PPT项目数据结构"""
    id: str
    title: str
    topic: str
    target_audience: str
    slide_count: int
    style_preference: str
    requirements: List[str]
    subtasks: List[SubTask]
    status: str = "planning"  # planning, in_progress, completed, failed


class PlannerAgent:
    """PPT任务规划智能体"""
    
    def __init__(self):
        # 创建模型
        model = OpenAIModel("gpt-4o-mini")
        
        # 创建完整的提示模板
        planning_prompt = PlanningPromptTemplate(
            initial_plan="请根据以下要求制定一个详细的计划来完成任务：{task_description}",
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
        self.projects: Dict[str, PPTProject] = {}
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """
        你是一个专业的PPT项目规划专家，负责将PPT生成任务拆分成多个子任务并分配给合适的agent处理。
        
        你的主要职责：
        1. 分析PPT项目需求和要求
        2. 将项目拆分成多个可执行的子任务
        3. 估算每个任务的完成时间
        4. 为任务分配合适的agent
        5. 创建项目时间线
        6. 验证任务计划的合理性
        
        可用的任务类型：
        - research: 资料收集和调研
        - content: 内容撰写和编辑
        - design: 幻灯片设计和布局
        - image: 图片生成和处理
        - review: 审查和编辑
        - assembly: 最终组装和优化
        
        请根据项目的具体需求，创建详细的任务分解计划。
        """
    
    def analyze_requirements(self, project_description: str) -> str:
        """分析PPT项目需求，提取关键信息
        
        Args:
            project_description: 项目描述，包含主题、目标受众、要求等
            
        Returns:
            分析结果，包含项目关键信息
        """
        try:
            # 使用智能体分析需求
            analysis_prompt = f"""
            请分析以下PPT项目需求，提取关键信息：
            
            {project_description}
            
            请提取以下信息：
            1. 项目主题
            2. 目标受众
            3. 预期幻灯片数量
            4. 风格偏好
            5. 特殊要求
            6. 时间限制
            7. 技术难度
            
            请以JSON格式返回分析结果。
            """
            
            response = self.agent.run(analysis_prompt)
            return response
            
        except Exception as e:
            logger.error(f"分析需求时出错: {e}")
            return f"分析需求时出错: {str(e)}"
    
    def create_task_breakdown(self, project_info: str) -> str:
        """创建任务分解计划
        
        Args:
            project_info: 项目信息（JSON格式）
            
        Returns:
            任务分解计划
        """
        try:
            breakdown_prompt = f"""
            基于以下项目信息，创建详细的任务分解计划：
            
            {project_info}
            
            请创建以下类型的子任务：
            1. 资料收集任务（research）
            2. 内容撰写任务（content）
            3. 幻灯片设计任务（design）
            4. 图片生成任务（image）
            5. 审查编辑任务（review）
            6. 最终组装任务（assembly）
            
            对于每个任务，请指定：
            - 任务ID
            - 任务类型
            - 任务标题
            - 任务描述
            - 依赖关系
            - 预计完成时间
            - 优先级
            
            请以JSON格式返回任务分解计划。
            """
            
            response = self.agent.run(breakdown_prompt)
            return response
            
        except Exception as e:
            logger.error(f"创建任务分解时出错: {e}")
            return f"创建任务分解时出错: {str(e)}"
    
    def estimate_task_duration(self, task_description: str, task_type: str) -> str:
        """估算任务完成时间
        
        Args:
            task_description: 任务描述
            task_type: 任务类型
            
        Returns:
            估算的完成时间（分钟）
        """
        try:
            estimation_prompt = f"""
            请估算以下任务的完成时间：
            
            任务类型: {task_type}
            任务描述: {task_description}
            
            请考虑以下因素：
            1. 任务复杂度
            2. 所需技能水平
            3. 资源可用性
            4. 质量要求
            
            请返回估算的分钟数。
            """
            
            response = self.agent.run(estimation_prompt)
            return response
            
        except Exception as e:
            logger.error(f"估算任务时间时出错: {e}")
            return f"估算任务时间时出错: {str(e)}"
    
    def assign_tasks_to_agents(self, task_list: str, available_agents: str) -> str:
        """为任务分配合适的agent
        
        Args:
            task_list: 任务列表（JSON格式）
            available_agents: 可用agent列表（JSON格式）
            
        Returns:
            任务分配方案
        """
        try:
            assignment_prompt = f"""
            请为以下任务分配合适的agent：
            
            任务列表:
            {task_list}
            
            可用agent:
            {available_agents}
            
            请考虑以下因素：
            1. agent的专业技能
            2. agent的当前工作负载
            3. 任务的优先级
            4. 任务的依赖关系
            
            请返回任务分配方案（JSON格式）。
            """
            
            response = self.agent.run(assignment_prompt)
            return response
            
        except Exception as e:
            logger.error(f"分配任务时出错: {e}")
            return f"分配任务时出错: {str(e)}"
    
    def create_project_timeline(self, task_assignments: str) -> str:
        """创建项目时间线
        
        Args:
            task_assignments: 任务分配方案（JSON格式）
            
        Returns:
            项目时间线
        """
        try:
            timeline_prompt = f"""
            基于以下任务分配方案，创建项目时间线：
            
            {task_assignments}
            
            请考虑：
            1. 任务的依赖关系
            2. 并行执行的可能性
            3. 关键路径
            4. 里程碑节点
            
            请创建详细的时间线，包括：
            - 每个任务的开始和结束时间
            - 里程碑节点
            - 关键路径
            - 缓冲时间
            
            请以JSON格式返回时间线。
            """
            
            response = self.agent.run(timeline_prompt)
            return response
            
        except Exception as e:
            logger.error(f"创建时间线时出错: {e}")
            return f"创建时间线时出错: {str(e)}"
    
    def validate_task_plan(self, complete_plan: str) -> str:
        """验证任务计划的合理性
        
        Args:
            complete_plan: 完整的任务计划（JSON格式）
            
        Returns:
            验证结果和建议
        """
        try:
            validation_prompt = f"""
            请验证以下任务计划的合理性：
            
            {complete_plan}
            
            请检查：
            1. 任务分解是否完整
            2. 依赖关系是否正确
            3. 时间估算是否合理
            4. 资源分配是否均衡
            5. 是否存在冲突
            6. 风险点识别
            
            请返回验证结果和改进建议。
            """
            
            response = self.agent.run(validation_prompt)
            return response
            
        except Exception as e:
            logger.error(f"验证计划时出错: {e}")
            return f"验证计划时出错: {str(e)}"
    
    def create_ppt_project(self, 
                          title: str, 
                          topic: str, 
                          target_audience: str, 
                          slide_count: int,
                          style_preference: str = "professional",
                          requirements: List[str] = None) -> str:
        """创建PPT项目并生成任务计划
        
        Args:
            title: 项目标题
            topic: 主题
            target_audience: 目标受众
            slide_count: 幻灯片数量
            style_preference: 风格偏好
            requirements: 特殊要求列表
            
        Returns:
            项目ID和任务计划
        """
        try:
            # 构建项目描述
            project_description = f"""
            项目标题: {title}
            主题: {topic}
            目标受众: {target_audience}
            幻灯片数量: {slide_count}
            风格偏好: {style_preference}
            特殊要求: {', '.join(requirements or [])}
            """
            
            # 分析需求
            logger.info("开始分析项目需求...")
            requirements_analysis = self.analyze_requirements(project_description)
            
            # 创建任务分解
            logger.info("创建任务分解...")
            task_breakdown = self.create_task_breakdown(requirements_analysis)
            
            # 定义可用agent
            available_agents = [
                {"id": "researcher", "name": "Research Agent", "skills": ["research", "data_analysis"]},
                {"id": "writer", "name": "Content Writer", "skills": ["writing", "editing"]},
                {"id": "designer", "name": "Design Agent", "skills": ["design", "layout"]},
                {"id": "image_gen", "name": "Image Generator", "skills": ["image_generation"]},
                {"id": "reviewer", "name": "Review Agent", "skills": ["review", "quality_check"]},
                {"id": "assembler", "name": "Assembly Agent", "skills": ["assembly", "optimization"]}
            ]
            
            # 分配任务
            logger.info("分配任务给agent...")
            task_assignments = self.assign_tasks_to_agents(task_breakdown, json.dumps(available_agents))
            
            # 创建时间线
            logger.info("创建项目时间线...")
            timeline = self.create_project_timeline(task_assignments)
            
            # 验证计划
            logger.info("验证任务计划...")
            complete_plan = {
                "requirements_analysis": requirements_analysis,
                "task_breakdown": task_breakdown,
                "task_assignments": task_assignments,
                "timeline": timeline
            }
            validation_result = self.validate_task_plan(json.dumps(complete_plan))
            
            # 生成项目ID
            import uuid
            project_id = str(uuid.uuid4())[:8]
            
            # 保存项目信息
            self.projects[project_id] = PPTProject(
                id=project_id,
                title=title,
                topic=topic,
                target_audience=target_audience,
                slide_count=slide_count,
                style_preference=style_preference,
                requirements=requirements or [],
                subtasks=[]  # 这里可以解析task_breakdown来填充
            )
            
            result = {
                "project_id": project_id,
                "status": "planned",
                "plan": complete_plan,
                "validation": validation_result
            }
            
            logger.info(f"项目 {project_id} 规划完成")
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.error(f"创建PPT项目时出错: {e}")
            return f"创建PPT项目时出错: {str(e)}"
    
    def get_project_status(self, project_id: str) -> str:
        """获取项目状态
        
        Args:
            project_id: 项目ID
            
        Returns:
            项目状态信息
        """
        if project_id not in self.projects:
            return f"项目 {project_id} 不存在"
        
        project = self.projects[project_id]
        return json.dumps({
            "project_id": project.id,
            "title": project.title,
            "status": project.status,
            "subtasks_count": len(project.subtasks),
            "completed_tasks": len([t for t in project.subtasks if t.status == "completed"])
        }, ensure_ascii=False, indent=2)
    
    def update_task_status(self, project_id: str, task_id: str, status: str, result: str = None) -> str:
        """更新任务状态
        
        Args:
            project_id: 项目ID
            task_id: 任务ID
            status: 新状态
            result: 任务结果
            
        Returns:
            更新结果
        """
        if project_id not in self.projects:
            return f"项目 {project_id} 不存在"
        
        project = self.projects[project_id]
        for task in project.subtasks:
            if task.id == task_id:
                task.status = status
                if result:
                    task.result = result
                return f"任务 {task_id} 状态已更新为 {status}"
        
        return f"任务 {task_id} 不存在"


def create_planner_agent() -> PlannerAgent:
    """创建planner agent实例"""
    return PlannerAgent()


if __name__ == "__main__":
    # 测试planner agent
    planner = create_planner_agent()
    
    # 创建示例项目
    result = planner.create_ppt_project(
        title="人工智能发展趋势报告",
        topic="AI技术的最新发展和未来趋势",
        target_audience="技术管理者和决策者",
        slide_count=20,
        style_preference="modern",
        requirements=["包含最新数据", "有图表展示", "适合演讲"]
    )
    
    print("PPT项目规划结果:")
    print(result)
