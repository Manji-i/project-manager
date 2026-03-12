#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timedelta
import os

PROJECT_DIR = "/root/.openclaw/workspace/skills/project-manager/references/projects/"

def load_project(project_id):
    path = os.path.join(PROJECT_DIR, f"{project_id}.json")
    if not os.path.exists(path):
        print(f"❌ 项目ID {project_id} 不存在")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f), path

def save_project(project, path):
    project['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)

def update_progress(project_id, task_id, progress, remark=""):
    project, path = load_project(project_id)
    progress = int(progress)
    found = False
    for task in project['tasks']:
        if task['task_id'] == task_id:
            found = True
            task['progress'] = progress
            if progress == 100:
                task['status'] = "completed"
            elif progress > 0:
                task['status'] = "in_progress"
            else:
                task['status'] = "not_started"
            if remark:
                task['remark'] = remark
            break
    if not found:
        print(f"❌ 任务ID {task_id} 不存在")
        sys.exit(1)
    # 计算整体进度
    total_progress = sum(t['progress'] for t in project['tasks']) / len(project['tasks'])
    project['overall_progress'] = round(total_progress, 1)
    # 更新项目状态
    if project['overall_progress'] == 100:
        project['status'] = "completed"
    elif project['overall_progress'] > 0:
        project['status'] = "in_progress"
    save_project(project, path)
    print(f"✅ 任务 {task_id} 进度已更新为 {progress}%")
    print(f"📊 项目整体进度：{project['overall_progress']}%")

def show_progress(project_id):
    project, _ = load_project(project_id)
    print(f"📋 项目：{project['project_name']}")
    print(f"⏰ 时间范围：{project['start_time']} 至 {project['end_time']}")
    print(f"📊 整体进度：{project['overall_progress']}% | 状态：{project['status']}")
    print(f"👥 负责人：{', '.join(project['owners'])}")
    print("\n任务列表：")
    for task in project['tasks']:
        status_emoji = {"not_started": "⚪", "in_progress": "🟡", "completed": "🟢"}.get(task['status'], "⚪")
        print(f"\n{status_emoji} {task['task_id']} {task['name']}")
        print(f"   负责人：{task['owner']} | 进度：{task['progress']}% | 时间：{task['start_time']} 至 {task['end_time']}")
        print(f"   交付物：{task['deliverable']}")
        if task['remark']:
            print(f"   备注：{task['remark']}")

def check_risk(project_id):
    project, _ = load_project(project_id)
    now = datetime.now()
    risks = []
    for task in project['tasks']:
        end_dt = datetime.strptime(task['end_time'], '%Y-%m-%d')
        # 检查延期风险
        if task['status'] != "completed" and end_dt < now:
            risks.append(f"🔴 任务 [{task['task_id']} {task['name']}] 已逾期，当前进度 {task['progress']}%，负责人：{task['owner']}")
        elif task['status'] == "not_started" and (end_dt - now).days < 3:
            risks.append(f"🟡 任务 [{task['task_id']} {task['name']}] 距离截止还有不到3天，尚未启动，负责人：{task['owner']}")
        elif task['status'] == "in_progress" and task['progress'] < 50 and (end_dt - now).days < 2:
            risks.append(f"🟡 任务 [{task['task_id']} {task['name']}] 距离截止还有不到2天，进度仅 {task['progress']}%，负责人：{task['owner']}")
    if not risks:
        print("✅ 项目无风险，所有任务进展正常")
    else:
        print("⚠️  项目风险预警：")
        for risk in risks:
            print(risk)
        print("\n💡 建议解决方案：")
        print("1. 立即联系对应负责人确认卡点，协调资源解决")
        print("2. 评估对整体项目的影响，必要时调整排期")
        print("3. 增加同步频次，每日跟进进度")
    return risks

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：")
        print("  更新进度：python progress_tracker.py update <项目ID> <任务ID> <完成率> [备注]")
        print("  查看进度：python progress_tracker.py show <项目ID>")
        print("  风险检查：python progress_tracker.py check_risk <项目ID>")
        print("\n示例：")
        print("  python progress_tracker.py update 20260312180000 T01 100 \"需求对齐完成\"")
        print("  python progress_tracker.py show 20260312180000")
        print("  python progress_tracker.py check_risk 20260312180000")
        sys.exit(1)
    action = sys.argv[1]
    project_id = sys.argv[2]
    if action == "update":
        if len(sys.argv) < 5:
            print("❌ 缺少参数，更新进度需要：<任务ID> <完成率>")
            sys.exit(1)
        task_id = sys.argv[3]
        progress = sys.argv[4]
        remark = sys.argv[5] if len(sys.argv) > 5 else ""
        update_progress(project_id, task_id, progress, remark)
    elif action == "show":
        show_progress(project_id)
    elif action == "check_risk":
        check_risk(project_id)
    else:
        print(f"❌ 不支持的操作：{action}")
        sys.exit(1)
