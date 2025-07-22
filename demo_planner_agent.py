#!/usr/bin/env python3
"""
演示版本的Planner Agent - 不依赖LLM调用，展示完整功能
"""

import sys
import os
import json
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


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


class DemoPlannerAgent:
    """演示版本的PPT任务规划智能体"""
    
    def __init__(self):
        self.projects: Dict[str, PPTProject] = {}
        self.available_agents = [
            {"id": "researcher", "name": "Research Agent", "skills": ["research", "data_analysis"]},
            {"id": "writer", "name": "Content Writer", "skills": ["writing", "editing"]},
            {"id": "designer", "name": "Design Agent", "skills": ["design", "layout"]},
            {"id": "image_gen", "name": "Image Generator", "skills": ["image_generation"]},
            {"id": "reviewer", "name": "Review Agent", "skills": ["review", "quality_check"]},
            {"id": "assembler", "name": "Assembly Agent", "skills": ["assembly", "optimization"]}
        ]
    
    def analyze_requirements(self, project_description: str) -> str:
        """分析PPT项目需求，提取关键信息"""
        # 模拟需求分析结果
        analysis_result = {
            "project_title": "人工智能发展趋势报告",
            "topic": "AI技术的最新发展和未来趋势",
            "target_audience": "技术管理者和决策者",
            "slide_count": 20,
            "style_preference": "modern",
            "requirements": ["包含最新数据", "有图表展示", "适合演讲"],
            "time_limit": "2周",
            "complexity": "中等"
        }
        return json.dumps(analysis_result, ensure_ascii=False, indent=2)
    
    def create_task_breakdown(self, project_info: str) -> str:
        """创建任务分解计划"""
        # 模拟任务分解结果
        tasks = [
            {
                "id": "task_001",
                "type": "research",
                "title": "收集AI发展趋势资料",
                "description": "收集人工智能领域的最新发展趋势、技术突破和市场数据",
                "dependencies": [],
                "estimated_duration": 120,
                "priority": 1
            },
            {
                "id": "task_002",
                "type": "content",
                "title": "撰写PPT内容大纲",
                "description": "基于收集的资料，撰写PPT的内容大纲和详细内容",
                "dependencies": ["task_001"],
                "estimated_duration": 180,
                "priority": 2
            },
            {
                "id": "task_003",
                "type": "design",
                "title": "设计幻灯片模板",
                "description": "设计现代化的幻灯片模板和布局",
                "dependencies": [],
                "estimated_duration": 90,
                "priority": 2
            },
            {
                "id": "task_004",
                "type": "image",
                "title": "生成图表和图片",
                "description": "生成数据图表、流程图和相关图片",
                "dependencies": ["task_001", "task_002"],
                "estimated_duration": 150,
                "priority": 3
            },
            {
                "id": "task_005",
                "type": "review",
                "title": "审查和编辑内容",
                "description": "审查PPT内容的准确性、逻辑性和表达效果",
                "dependencies": ["task_002", "task_004"],
                "estimated_duration": 60,
                "priority": 4
            },
            {
                "id": "task_006",
                "type": "assembly",
                "title": "最终组装和优化",
                "description": "将所有内容组装成完整的PPT，进行最终优化",
                "dependencies": ["task_003", "task_005"],
                "estimated_duration": 120,
                "priority": 5
            }
        ]
        
        return json.dumps({"tasks": tasks}, ensure_ascii=False, indent=2)
    
    def assign_tasks_to_agents(self, task_list: str, available_agents: str) -> str:
        """为任务分配合适的agent"""
        # 模拟任务分配结果
        assignments = {
            "assignments": [
                {"task_id": "task_001", "agent_id": "researcher", "reason": "专业资料收集"},
                {"task_id": "task_002", "agent_id": "writer", "reason": "内容撰写专业"},
                {"task_id": "task_003", "agent_id": "designer", "reason": "设计布局专业"},
                {"task_id": "task_004", "agent_id": "image_gen", "reason": "图片生成专业"},
                {"task_id": "task_005", "agent_id": "reviewer", "reason": "质量审查专业"},
                {"task_id": "task_006", "agent_id": "assembler", "reason": "最终组装专业"}
            ]
        }
        return json.dumps(assignments, ensure_ascii=False, indent=2)
    
    def create_project_timeline(self, task_assignments: str) -> str:
        """创建项目时间线"""
        # 模拟时间线结果
        timeline = {
            "timeline": [
                {
                    "task_id": "task_001",
                    "start_time": "Day 1 09:00",
                    "end_time": "Day 1 11:00",
                    "duration": "2小时"
                },
                {
                    "task_id": "task_003",
                    "start_time": "Day 1 14:00",
                    "end_time": "Day 1 15:30",
                    "duration": "1.5小时"
                },
                {
                    "task_id": "task_002",
                    "start_time": "Day 2 09:00",
                    "end_time": "Day 2 12:00",
                    "duration": "3小时"
                },
                {
                    "task_id": "task_004",
                    "start_time": "Day 2 14:00",
                    "end_time": "Day 2 16:30",
                    "duration": "2.5小时"
                },
                {
                    "task_id": "task_005",
                    "start_time": "Day 3 09:00",
                    "end_time": "Day 3 10:00",
                    "duration": "1小时"
                },
                {
                    "task_id": "task_006",
                    "start_time": "Day 3 14:00",
                    "end_time": "Day 3 16:00",
                    "duration": "2小时"
                }
            ],
            "milestones": [
                {"name": "资料收集完成", "time": "Day 1 11:00"},
                {"name": "内容撰写完成", "time": "Day 2 12:00"},
                {"name": "设计完成", "time": "Day 2 16:30"},
                {"name": "最终交付", "time": "Day 3 16:00"}
            ],
            "critical_path": ["task_001", "task_002", "task_004", "task_005", "task_006"],
            "total_duration": "3天"
        }
        return json.dumps(timeline, ensure_ascii=False, indent=2)
    
    def validate_task_plan(self, complete_plan: str) -> str:
        """验证任务计划的合理性"""
        # 模拟验证结果
        validation_result = {
            "status": "valid",
            "issues": [],
            "suggestions": [
                "任务分解完整，覆盖了PPT制作的所有关键环节",
                "依赖关系合理，符合制作流程",
                "时间估算适中，考虑了任务复杂度",
                "资源分配均衡，每个agent都有合适的任务",
                "建议增加10%的缓冲时间以应对意外情况"
            ],
            "risks": [
                "资料收集可能遇到信息不足的情况",
                "图片生成可能需要多次调整",
                "审查过程可能需要多轮修改"
            ],
            "overall_score": 85
        }
        return json.dumps(validation_result, ensure_ascii=False, indent=2)
    
    def create_ppt_project(self, 
                          title: str, 
                          topic: str, 
                          target_audience: str, 
                          slide_count: int,
                          style_preference: str = "professional",
                          requirements: List[str] = None) -> str:
        """创建PPT项目并生成任务计划"""
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
            
            print("开始分析项目需求...")
            requirements_analysis = self.analyze_requirements(project_description)
            
            print("创建任务分解...")
            task_breakdown = self.create_task_breakdown(requirements_analysis)
            
            print("分配任务给agent...")
            task_assignments = self.assign_tasks_to_agents(task_breakdown, json.dumps(self.available_agents))
            
            print("创建项目时间线...")
            timeline = self.create_project_timeline(task_assignments)
            
            print("验证任务计划...")
            complete_plan = {
                "requirements_analysis": requirements_analysis,
                "task_breakdown": task_breakdown,
                "task_assignments": task_assignments,
                "timeline": timeline
            }
            validation_result = self.validate_task_plan(json.dumps(complete_plan))
            
            # 生成项目ID
            project_id = str(uuid.uuid4())[:8]
            
            # 创建子任务列表
            task_data = json.loads(task_breakdown)
            subtasks = []
            for task_info in task_data.get("tasks", []):
                subtask = SubTask(
                    id=task_info["id"],
                    type=TaskType(task_info["type"]),
                    title=task_info["title"],
                    description=task_info["description"],
                    dependencies=task_info["dependencies"],
                    estimated_duration=task_info["estimated_duration"],
                    priority=task_info["priority"]
                )
                subtasks.append(subtask)
            
            # 保存项目信息
            self.projects[project_id] = PPTProject(
                id=project_id,
                title=title,
                topic=topic,
                target_audience=target_audience,
                slide_count=slide_count,
                style_preference=style_preference,
                requirements=requirements or [],
                subtasks=subtasks
            )
            
            result = {
                "project_id": project_id,
                "status": "planned",
                "plan": complete_plan,
                "validation": validation_result
            }
            
            print(f"项目 {project_id} 规划完成")
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return f"创建PPT项目时出错: {str(e)}"
    
    def get_project_status(self, project_id: str) -> str:
        """获取项目状态"""
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
        """更新任务状态"""
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


def main():
    """主函数 - 演示Planner Agent的完整功能"""
    print("=" * 60)
    print("演示版本的Planner Agent")
    print("=" * 60)
    
    # 创建planner agent
    planner = DemoPlannerAgent()
    
    # 创建PPT项目
    print("\n1. 创建PPT项目")
    print("-" * 30)
    
    result = planner.create_ppt_project(
        title="人工智能发展趋势报告",
        topic="AI技术的最新发展和未来趋势",
        target_audience="技术管理者和决策者",
        slide_count=20,
        style_preference="modern",
        requirements=["包含最新数据", "有图表展示", "适合演讲"]
    )
    
    print("项目创建结果:")
    print(result)
    
    # 解析项目ID
    try:
        result_data = json.loads(result)
        project_id = result_data.get("project_id")
        
        if project_id:
            print(f"\n项目ID: {project_id}")
            
            # 获取项目状态
            status = planner.get_project_status(project_id)
            print(f"项目状态: {status}")
            
            # 模拟任务执行
            print("\n2. 模拟任务执行")
            print("-" * 30)
            
            # 更新任务状态
            tasks_to_update = [
                ("task_001", "completed", "资料收集完成，包含最新的AI发展趋势数据"),
                ("task_002", "completed", "内容撰写完成，包含详细的技术分析"),
                ("task_003", "completed", "设计模板完成，采用现代化风格"),
                ("task_004", "in_progress", "正在生成图表和图片"),
                ("task_005", "pending", "等待内容完成后进行审查"),
                ("task_006", "pending", "等待所有前置任务完成后进行组装")
            ]
            
            for task_id, status, result in tasks_to_update:
                update_result = planner.update_task_status(project_id, task_id, status, result)
                print(update_result)
            
            # 获取最终状态
            final_status = planner.get_project_status(project_id)
            print(f"\n最终项目状态: {final_status}")
            
    except json.JSONDecodeError:
        print("无法解析项目创建结果")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main() 