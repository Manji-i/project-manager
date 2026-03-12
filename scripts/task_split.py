#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict

def split_task(project_desc, time_range, owners):
    owners = [o.strip() for o in owners.split(',') if o.strip()]
    start_date, end_date = [d.strip() for d in time_range.split('至')]
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    total_days = (end_dt - start_dt).days

    # 默认拆解模板，可根据项目类型调整
    task_templates = [
        {"name": "项目需求调研与对齐", "duration_ratio": 0.15, "deliverable": "需求文档/对齐纪要", "acceptance": "所有相关方签字确认需求"},
        {"name": "方案设计与评审", "duration_ratio": 0.2, "deliverable": "项目方案文档", "acceptance": "方案评审通过"},
        {"name": "资源协调与准备", "duration_ratio": 0.1, "deliverable": "资源到位确认清单", "acceptance": "人力/预算/权限全部到位"},
        {"name": "核心功能开发/执行", "duration_ratio": 0.35, "deliverable": "可交付的核心产出物", "acceptance": "功能测试通过/执行结果达标"},
        {"name": "测试/验收", "duration_ratio": 0.15, "deliverable": "测试报告/验收报告", "acceptance": "验收通过"},
        {"name": "项目上线/交付", "duration_ratio": 0.05, "deliverable": "交付物/上线纪要", "acceptance": "用户确认接收交付"},
    ]

    tasks = []
    current_dt = start_dt
    for i, template in enumerate(task_templates):
        task_days = max(1, int(total_days * template['duration_ratio']))
        task_end_dt = current_dt + timedelta(days=task_days - 1)
        if task_end_dt > end_dt:
            task_end_dt = end_dt
        owner = owners[i % len(owners)] if owners else "待分配"
        task = {
            "task_id": f"T{i+1:02d}",
            "name": template['name'],
            "owner": owner,
            "start_time": current_dt.strftime('%Y-%m-%d'),
            "end_time": task_end_dt.strftime('%Y-%m-%d'),
            "duration_days": task_days,
            "deliverable": template['deliverable'],
            "acceptance": template['acceptance'],
            "status": "not_started",
            "progress": 0,
            "remark": ""
        }
        tasks.append(task)
        current_dt = task_end_dt + timedelta(days=1)
        if current_dt > end_dt:
            break

    project = {
        "project_name": project_desc[:20] + "..." if len(project_desc) > 20 else project_desc,
        "project_desc": project_desc,
        "start_time": start_date,
        "end_time": end_date,
        "total_days": total_days,
        "owners": owners,
        "tasks": tasks,
        "overall_progress": 0,
        "status": "init",
        "create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # 保存项目文件
    project_id = datetime.now().strftime('%Y%m%d%H%M%S')
    save_path = f"/root/.openclaw/workspace/skills/project-manager/references/projects/{project_id}.json"
    import os
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)

    # 输出任务清单
    print(f"✅ 项目初始化完成，项目ID：{project_id}")
    print(f"📋 任务拆解清单：")
    for task in tasks:
        print(f"\n{task['task_id']} {task['name']}")
        print(f"   负责人：{task['owner']} | 时间：{task['start_time']} 至 {task['end_time']}")
        print(f"   交付物：{task['deliverable']} | 验收标准：{task['acceptance']}")
    print(f"\n📁 项目文件已保存到：{save_path}")
    return project_id

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法：python task_split.py \"项目描述\" \"开始时间至结束时间\" \"负责人1,负责人2,...\"")
        print("示例：python task_split.py \"清北招聘项目突破\" \"2026-03-12至2026-03-31\" \"庄凯芸,王恂\"")
        sys.exit(1)
    project_desc = sys.argv[1]
    time_range = sys.argv[2]
    owners = sys.argv[3]
    split_task(project_desc, time_range, owners)
