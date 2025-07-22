#!/usr/bin/env python3
"""
示例：完整的PPT生成系统，使用Planner Agent进行任务规划
"""

import sys
import os
import json
import time
from typing import Dict, List, Any

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.planner_agent import create_planner_agent
from tools.web_search import web_search, fetch_webpage_content
from loguru import logger


class PPTGenerationSystem:
    """PPT生成系统"""
    
    def __init__(self):
        self.planner = create_planner_agent()
        self.projects: Dict[str, Dict[str, Any]] = {}
        self.agents = {
            "researcher": self._research_agent,
            "writer": self._content_writer_agent,
            "designer": self._design_agent,
            "image_gen": self._image_generator_agent,
            "reviewer": self._review_agent,
            "assembler": self._assembly_agent
        }
    
    def create_project(self, 
                      title: str, 
                      topic: str, 
                      target_audience: str, 
                      slide_count: int,
                      style_preference: str = "professional",
                      requirements: List[str] = None) -> str:
        """创建PPT项目"""
        logger.info(f"创建PPT项目: {title}")
        
        result = self.planner.create_ppt_project(
            title=title,
            topic=topic,
            target_audience=target_audience,
            slide_count=slide_count,
            style_preference=style_preference,
            requirements=requirements
        )
        
        try:
            result_data = json.loads(result)
            project_id = result_data.get("project_id")
            if project_id:
                self.projects[project_id] = {
                    "plan": result_data,
                    "status": "created",
                    "tasks": {},
                    "results": {}
                }
                logger.info(f"项目 {project_id} 创建成功")
            
            return result
            
        except json.JSONDecodeError:
            logger.error("无法解析项目创建结果")
            return result
    
    def execute_project(self, project_id: str) -> str:
        """执行PPT项目"""
        if project_id not in self.projects:
            return f"项目 {project_id} 不存在"
        
        logger.info(f"开始执行项目 {project_id}")
        
        try:
            project = self.projects[project_id]
            plan = project["plan"]
            
            # 解析任务计划
            task_assignments = plan.get("plan", {}).get("task_assignments", "{}")
            task_data = json.loads(task_assignments)
            
            # 执行任务
            for task_info in task_data.get("tasks", []):
                task_id = task_info.get("id")
                task_type = task_info.get("type")
                assigned_agent = task_info.get("assigned_agent")
                
                if task_id and task_type and assigned_agent:
                    logger.info(f"执行任务 {task_id} ({task_type}) 分配给 {assigned_agent}")
                    
                    # 执行任务
                    result = self._execute_task(task_id, task_type, task_info)
                    
                    # 更新任务状态
                    self.planner.update_task_status(project_id, task_id, "completed", result)
                    project["tasks"][task_id] = {
                        "status": "completed",
                        "result": result
                    }
                    
                    # 模拟任务执行时间
                    time.sleep(1)
            
            # 更新项目状态
            project["status"] = "completed"
            logger.info(f"项目 {project_id} 执行完成")
            
            return f"项目 {project_id} 执行完成"
            
        except Exception as e:
            logger.error(f"执行项目时出错: {e}")
            return f"执行项目时出错: {str(e)}"
    
    def _execute_task(self, task_id: str, task_type: str, task_info: Dict[str, Any]) -> str:
        """执行单个任务"""
        try:
            if task_type in self.agents:
                return self.agents[task_type](task_info)
            else:
                return f"未知任务类型: {task_type}"
        except Exception as e:
            logger.error(f"执行任务 {task_id} 时出错: {e}")
            return f"任务执行失败: {str(e)}"
    
    def _research_agent(self, task_info: Dict[str, Any]) -> str:
        """研究agent - 收集资料"""
        topic = task_info.get("description", "").split(":")[-1].strip()
        logger.info(f"研究agent开始收集资料: {topic}")
        
        # 使用网页搜索工具收集资料
        search_result = web_search(topic, max_results=5, include_content=True)
        
        return f"资料收集完成:\n{search_result}"
    
    def _content_writer_agent(self, task_info: Dict[str, Any]) -> str:
        """内容撰写agent - 撰写PPT内容"""
        logger.info("内容撰写agent开始工作")
        
        # 这里可以集成内容生成工具
        content = f"""
        # {task_info.get('title', 'PPT内容')}
        
        ## 主要内容
        - 要点1
        - 要点2
        - 要点3
        
        ## 详细说明
        这是根据任务要求生成的内容...
        """
        
        return content
    
    def _design_agent(self, task_info: Dict[str, Any]) -> str:
        """设计agent - 设计幻灯片布局"""
        logger.info("设计agent开始工作")
        
        design_spec = {
            "layout": "modern",
            "color_scheme": "professional",
            "typography": "clean",
            "spacing": "generous"
        }
        
        return f"设计规范:\n{json.dumps(design_spec, ensure_ascii=False, indent=2)}"
    
    def _image_generator_agent(self, task_info: Dict[str, Any]) -> str:
        """图片生成agent - 生成相关图片"""
        logger.info("图片生成agent开始工作")
        
        # 这里可以集成图片生成工具
        images = [
            "chart_1.png",
            "diagram_1.png",
            "illustration_1.png"
        ]
        
        return f"生成的图片: {', '.join(images)}"
    
    def _review_agent(self, task_info: Dict[str, Any]) -> str:
        """审查agent - 审查和编辑内容"""
        logger.info("审查agent开始工作")
        
        review_result = {
            "content_quality": "excellent",
            "suggestions": [
                "增加更多数据支持",
                "优化图表展示",
                "调整字体大小"
            ],
            "overall_score": 85
        }
        
        return f"审查结果:\n{json.dumps(review_result, ensure_ascii=False, indent=2)}"
    
    def _assembly_agent(self, task_info: Dict[str, Any]) -> str:
        """组装agent - 最终组装PPT"""
        logger.info("组装agent开始工作")
        
        assembly_result = {
            "total_slides": 20,
            "file_format": "pptx",
            "file_size": "2.5MB",
            "features": [
                "响应式设计",
                "动画效果",
                "交互元素"
            ]
        }
        
        return f"PPT组装完成:\n{json.dumps(assembly_result, ensure_ascii=False, indent=2)}"
    
    def get_project_status(self, project_id: str) -> str:
        """获取项目状态"""
        if project_id not in self.projects:
            return f"项目 {project_id} 不存在"
        
        project = self.projects[project_id]
        return json.dumps({
            "project_id": project_id,
            "status": project["status"],
            "tasks_count": len(project["tasks"]),
            "completed_tasks": len([t for t in project["tasks"].values() if t["status"] == "completed"])
        }, ensure_ascii=False, indent=2)


def main():
    """主函数 - 演示完整的PPT生成流程"""
    print("=" * 60)
    print("PPT生成系统演示")
    print("=" * 60)
    
    # 创建PPT生成系统
    system = PPTGenerationSystem()
    
    # 创建PPT项目
    print("\n1. 创建PPT项目")
    print("-" * 30)
    
    result = system.create_project(
        title="人工智能在医疗领域的应用",
        topic="AI技术在医疗诊断、药物研发和患者管理中的应用",
        target_audience="医疗行业专业人士",
        slide_count=25,
        style_preference="modern",
        requirements=["包含最新案例", "有数据支持", "适合学术会议"]
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
            status = system.get_project_status(project_id)
            print(f"项目状态: {status}")
            
            # 执行项目
            print("\n2. 执行PPT项目")
            print("-" * 30)
            
            execution_result = system.execute_project(project_id)
            print(f"执行结果: {execution_result}")
            
            # 获取最终状态
            final_status = system.get_project_status(project_id)
            print(f"\n最终项目状态: {final_status}")
            
    except json.JSONDecodeError:
        print("无法解析项目创建结果")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main() 