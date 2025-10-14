"""
配置管理模块

此模块定义了 Issue 分诊系统的配置，包括分类规则和开发者分配策略。
支持动态添加新的分类和分配规则。
"""

from typing import Dict, List


# 开发者分配规则字典
DEVELOPER_ASSIGNMENT: Dict[str, str] = {
    "Bug": "张三",
    "Feature Request": "李四",
    "Question": "王五",
}


class TriageConfig:
    """分诊配置类
    
    管理 Issue 分类和开发者分配的配置。支持动态添加新的分类规则。
    
    Attributes:
        categories: 支持的 Issue 分类列表
        assignments: 分类到开发者的映射字典
        default_assignee: 未知分类时的默认分配人
    """
    
    def __init__(self):
        """初始化配置实例"""
        self.categories: List[str] = [
            "Bug",
            "Feature Request",
            "Question",
        ]
        
        self.assignments: Dict[str, str] = DEVELOPER_ASSIGNMENT.copy()
        
        self.default_assignee: str = "项目负责人"
    
    def add_category(self, category: str, assignee: str) -> None:
        """动态添加新的分类和对应的分配人
        
        Args:
            category: 新的分类名称
            assignee: 负责该分类的开发者名称
            
        Example:
            config.add_category("Documentation", "赵六")
        """
        if category not in self.categories:
            self.categories.append(category)
        self.assignments[category] = assignee
    
    def get_assignee(self, category: str) -> str:
        """根据分类获取对应的分配人
        
        Args:
            category: Issue 分类
            
        Returns:
            分配的开发者名称，如果分类不存在则返回默认分配人
            
        Example:
            assignee = config.get_assignee("Bug")
            # Returns: "张三"
        """
        return self.assignments.get(category, self.default_assignee)


# 全局配置实例
config = TriageConfig()
