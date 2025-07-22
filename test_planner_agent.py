#!/usr/bin/env python3
"""
测试Planner Agent的功能
"""

import sys
import os
import json

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.planner_agent import create_planner_agent


def test_planner_agent():
    """测试planner agent的基本功能"""
    print("=" * 60)
    print("测试Planner Agent")
    print("=" * 60)
    
    # 创建planner agent
    planner = create_planner_agent()
    
    # 测试用例1：技术报告PPT
    print("\n1. 测试技术报告PPT项目")
    print("-" * 40)
    
    result1 = planner.create_ppt_project(
        title="人工智能发展趋势报告",
        topic="AI技术的最新发展和未来趋势",
        target_audience="技术管理者和决策者",
        slide_count=20,
        style_preference="modern",
        requirements=["包含最新数据", "有图表展示", "适合演讲"]
    )
    
    print("技术报告PPT规划结果:")
    print(result1)
    
    # 解析结果获取项目ID
    try:
        result_data = json.loads(result1)
        project_id = result_data.get("project_id")
        
        if project_id:
            print(f"\n项目ID: {project_id}")
            
            # 获取项目状态
            status = planner.get_project_status(project_id)
            print(f"项目状态: {status}")
            
    except json.JSONDecodeError:
        print("无法解析JSON结果")
    
    # 测试用例2：教育PPT
    print("\n\n2. 测试教育PPT项目")
    print("-" * 40)
    
    result2 = planner.create_ppt_project(
        title="Python编程入门教程",
        topic="Python基础语法和编程概念",
        target_audience="编程初学者",
        slide_count=15,
        style_preference="educational",
        requirements=["包含代码示例", "有互动元素", "适合课堂使用"]
    )
    
    print("教育PPT规划结果:")
    print(result2)
    
    # 测试用例3：商业提案PPT
    print("\n\n3. 测试商业提案PPT项目")
    print("-" * 40)
    
    result3 = planner.create_ppt_project(
        title="新产品市场推广方案",
        topic="智能家居产品的市场策略",
        target_audience="投资人和合作伙伴",
        slide_count=25,
        style_preference="professional",
        requirements=["包含市场分析", "有财务预测", "突出竞争优势"]
    )
    
    print("商业提案PPT规划结果:")
    print(result3)


def test_individual_tools():
    """测试planner agent的各个工具"""
    print("\n" + "=" * 60)
    print("测试Planner Agent的各个工具")
    print("=" * 60)
    
    planner = create_planner_agent()
    
    # 测试需求分析
    print("\n1. 测试需求分析工具")
    print("-" * 30)
    
    project_description = """
    项目标题: 机器学习应用案例分享
    主题: 机器学习在金融领域的实际应用
    目标受众: 金融行业从业者
    幻灯片数量: 18
    风格偏好: 专业商务风格
    特殊要求: 包含实际案例, 有数据可视化, 适合技术分享
    """
    
    analysis_result = planner.analyze_requirements(project_description)
    print("需求分析结果:")
    print(analysis_result)
    
    # 测试任务分解
    print("\n2. 测试任务分解工具")
    print("-" * 30)
    
    project_info = """
    {
        "project_title": "机器学习应用案例分享",
        "topic": "机器学习在金融领域的实际应用",
        "target_audience": "金融行业从业者",
        "slide_count": 18,
        "style_preference": "专业商务风格",
        "requirements": ["包含实际案例", "有数据可视化", "适合技术分享"]
    }
    """
    
    breakdown_result = planner.create_task_breakdown(project_info)
    print("任务分解结果:")
    print(breakdown_result)
    
    # 测试时间估算
    print("\n3. 测试时间估算工具")
    print("-" * 30)
    
    task_description = "收集机器学习在金融领域的最新应用案例和数据"
    task_type = "research"
    
    duration_result = planner.estimate_task_duration(task_description, task_type)
    print("时间估算结果:")
    print(duration_result)


def test_project_management():
    """测试项目管理功能"""
    print("\n" + "=" * 60)
    print("测试项目管理功能")
    print("=" * 60)
    
    planner = create_planner_agent()
    
    # 创建测试项目
    result = planner.create_ppt_project(
        title="测试项目管理功能",
        topic="测试主题",
        target_audience="测试用户",
        slide_count=10,
        style_preference="test",
        requirements=["测试要求"]
    )
    
    try:
        result_data = json.loads(result)
        project_id = result_data.get("project_id")
        
        if project_id:
            print(f"创建的项目ID: {project_id}")
            
            # 测试获取项目状态
            status = planner.get_project_status(project_id)
            print(f"项目状态: {status}")
            
            # 测试更新任务状态（这里需要先有任务）
            # update_result = planner.update_task_status(project_id, "task_001", "completed", "任务完成")
            # print(f"更新任务状态: {update_result}")
            
    except json.JSONDecodeError:
        print("无法解析项目创建结果")


def main():
    """主测试函数"""
    try:
        # 测试基本功能
        test_planner_agent()
        
        # 测试各个工具
        test_individual_tools()
        
        # 测试项目管理
        test_project_management()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 