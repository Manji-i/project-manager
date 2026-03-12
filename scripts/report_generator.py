#!/usr/bin/env python3
import json
import sys
from datetime import datetime
import os

PROJECT_DIR = "/root/.openclaw/workspace/skills/project-manager/references/projects/"

def load_project(project_id):
    path = os.path.join(PROJECT_DIR, f"{project_id}.json")
    if not os.path.exists(path):
        print(f"❌ 项目ID {project_id} 不存在")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_report(project_id, report_type):
    project = load_project(project_id)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_title = {
        "weekly": f"【周进度报告】{project['project_name']}（{now[:10]}）",
        "final": f"【项目复盘报告】{project['project_name']}"
    }[report_type]

    # 分类任务
    completed_tasks = [t for t in project['tasks'] if t['status'] == 'completed']
    in_progress_tasks = [t for t in project['tasks'] if t['status'] == 'in_progress']
    not_started_tasks = [t for t in project['tasks'] if t['status'] == 'not_started']

    # 生成报告内容
    report = f"# {report_title}\n\n"
    report += "## 项目概览\n"
    report += f"- 项目名称：{project['project_name']}\n"
    report += f"- 时间范围：{project['start_time']} 至 {project['end_time']}\n"
    report += f"- 整体进度：{project['overall_progress']}%\n"
    report += f"- 项目状态：{project['status']}\n"
    report += f"- 负责人：{', '.join(project['owners'])}\n\n"

    if report_type == "weekly":
        report += "## 本周完成情况\n"
        if completed_tasks:
            for task in completed_tasks:
                report += f"- ✅ {task['task_id']} {task['name']}（{task['progress']}%）\n"
                if task['remark']:
                    report += f"  备注：{task['remark']}\n"
        else:
            report += "- 本周无完成任务\n"
        
        report += "\n## 进行中任务\n"
        if in_progress_tasks:
            for task in in_progress_tasks:
                report += f"- 🟡 {task['task_id']} {task['name']}（{task['progress']}%），截止时间：{task['end_time']}，负责人：{task['owner']}\n"
        else:
            report += "- 无进行中任务\n"
        
        report += "\n## 待启动任务\n"
        if not_started_tasks:
            for task in not_started_tasks:
                report += f"- ⚪ {task['task_id']} {task['name']}，计划开始时间：{task['start_time']}，负责人：{task['owner']}\n"
        else:
            report += "- 无待启动任务\n"
        
        report += "\n## 风险与问题\n"
        # 调用风险检查
        from progress_tracker import check_risk
        risks = check_risk(project_id)
        if risks:
            for risk in risks:
                report += f"- {risk}\n"
        else:
            report += "- 无风险\n"
        
        report += "\n## 下周计划\n"
        next_tasks = in_progress_tasks + not_started_tasks[:3]
        if next_tasks:
            for task in next_tasks[:3]:
                report += f"- {task['task_id']} {task['name']}，目标进度：100%，负责人：{task['owner']}\n"
        else:
            report += "- 项目已完成，无后续计划\n"
    
    else: # final report
        report += "## 目标达成情况\n"
        report += f"- 计划完成时间：{project['end_time']}\n"
        report += f"- 实际完成时间：{now[:10]}\n"
        report += f"- 整体完成率：{project['overall_progress']}%\n"
        report += "- 核心交付物：\n"
        for task in completed_tasks:
            report += f"  - {task['deliverable']}\n\n"
        
        report += "## 亮点与经验\n"
        report += "- 待补充（可根据实际情况填写）\n\n"
        
        report += "## 待改进点\n"
        report += "- 待补充（可根据实际情况填写）\n\n"
        
        report += "## 后续行动建议\n"
        report += "- 待补充（可根据实际情况填写）\n"

    # 保存报告
    report_path = f"/root/.openclaw/workspace/skills/project-manager/references/projects/{project_id}_{report_type}_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ {report_title} 已生成")
    print(f"📁 报告路径：{report_path}")
    print("\n报告预览：")
    print("="*50)
    print(report[:500] + "..." if len(report) > 500 else report)
    return report_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python report_generator.py <项目ID> <报告类型:weekly/final>")
        print("示例：")
        print("  生成周报：python report_generator.py 20260312180000 weekly")
        print("  生成复盘报告：python report_generator.py 20260312180000 final")
        sys.exit(1)
    project_id = sys.argv[1]
    report_type = sys.argv[2]
    if report_type not in ["weekly", "final"]:
        print("❌ 报告类型只能是 weekly 或 final")
        sys.exit(1)
    generate_report(project_id, report_type)
