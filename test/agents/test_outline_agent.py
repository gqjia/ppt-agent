#!/usr/bin/env python3
"""
快速测试 outline_generate.py
"""
import os
import sys
import json
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.agents.outline_generate import outline_generate_agent


def safe_json_serialize(obj):
    """安全的 JSON 序列化函数，处理不可序列化的对象"""
    if obj is None:
        return None
    
    # 基本类型直接返回
    if isinstance(obj, (str, int, float, bool)):
        return obj
    
    # 列表类型递归处理
    if isinstance(obj, list):
        return [safe_json_serialize(item) for item in obj]
    
    # 字典类型递归处理
    if isinstance(obj, dict):
        return {key: safe_json_serialize(value) for key, value in obj.items()}
    
    # 对象类型转换为字典
    if hasattr(obj, '__dict__'):
        return {key: safe_json_serialize(value) for key, value in obj.__dict__.items()}
    
    # 其他类型转换为字符串
    return str(obj)


def load_test_cases():
    """加载测试用例"""
    dataset_path = os.path.join(os.path.dirname(__file__), "test_dataset.txt")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def run_test():
    """运行测试"""
    print("🚀 开始测试 Outline Generate Agent")
    
    # 加载测试用例
    test_cases = load_test_cases()
    print(f"📋 找到 {len(test_cases)} 个测试用例: {test_cases}")
    
    results = []
    
    for i, task in enumerate(test_cases, 1):
        print(f"\n🧪 测试用例 {i}/{len(test_cases)}: {task}")
        
        start_time = time.time()
        success = False
        error_msg = None
        result = None
        
        try:
            result = outline_generate_agent.run(task=task)
            success = True
            print(f"  ✅ 执行成功")
            
            # 将 RunResult 对象转换为可序列化的格式
            if hasattr(result, '__dict__'):
                # 如果是对象，尝试转换为字典
                serializable_result = {}
                for key, value in result.__dict__.items():
                    try:
                        # 测试是否可以序列化
                        json.dumps(value)
                        serializable_result[key] = value
                    except (TypeError, ValueError):
                        # 如果不能序列化，转换为字符串
                        serializable_result[key] = str(value)
                result = serializable_result
            else:
                # 如果不是对象，直接转换为字符串
                result = str(result)
                
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ 执行失败: {error_msg}")
        
        execution_time = time.time() - start_time
        print(f"  ⏱️  执行时间: {execution_time:.2f}秒")
        
        results.append({
            "task": task,
            "success": success,
            "execution_time": execution_time,
            "error": error_msg,
            "result": result if success else None
        })

    # 统计结果
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    
    print(f"\n📊 测试结果统计:")
    print(f"  总测试用例: {total}")
    print(f"  成功执行: {successful} ({successful/total*100:.1f}%)")
    
    # 保存结果
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    result_file = os.path.join(os.path.dirname(__file__), f"outline_results_{timestamp}.json")
    
    # 使用安全的序列化函数
    serializable_results = safe_json_serialize(results)
    
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, ensure_ascii=False, indent=2)
    
    print(f"📄 详细结果已保存到: {result_file}")
    
    return results


if __name__ == "__main__":
    run_test()