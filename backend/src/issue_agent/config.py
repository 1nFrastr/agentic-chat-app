"""
配置管理模块

定义 Issue 分诊系统的配置访问接口。
实际的配置数据定义在 models.py 中,确保与类型定义保持一致。
"""

from src.issue_agent.models import CATEGORY_ASSIGNMENTS, DEFAULT_ASSIGNEE


class TriageConfig:
    """分诊配置类
    
    提供统一的配置访问接口。
    配置数据定义在 models.py 中,与 CategoryType 保持对应关系。
    """
    
    def __init__(self):
        """初始化配置"""
        self.assignments = CATEGORY_ASSIGNMENTS
        self.default_assignee = DEFAULT_ASSIGNEE
    
    def get_assignee(self, category: str) -> str:
        """根据分类获取对应的分配人
        
        Args:
            category: Issue 分类
            
        Returns:
            分配的开发者名称,如果分类不存在则返回默认分配人
        """
        return self.assignments.get(category, self.default_assignee)


# 全局配置实例
config = TriageConfig()



