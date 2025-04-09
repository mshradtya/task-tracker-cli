import cmd
import json
import os
from datetime import datetime

class TaskTracker(cmd.Cmd):
    prompt = 'task-cli '
    intro = 'Welcome to task-tracker'
    status = ['todo', 'in-progress', 'done']
    file_name = 'tasks.json'

    def get_tasks(self):
        if not os.path.exists(self.file_name):
            return []
        try:
            with open(self.file_name, 'r') as f:
                return json.load(f).get('tasks', [])
        except json.JSONDecodeError:
            return []
        
    def get_next_id(self, tasks):
        return max([task["id"] for task in tasks], default=0) + 1

    def save_tasks(self, tasks):
        with open(self.file_name, 'w') as f:
            json.dump({"tasks": tasks}, f, indent=4)

    def get_next_id(self, tasks):
        return max([task["id"] for task in tasks], default=0) + 1

    def do_add(self, arg):
        desc = arg.strip()
        if not desc:
            print('task description cannot be empty')
            return
        
        tasks = self.get_tasks()
        task_id = self.get_next_id(tasks)
        timestamp = datetime.now().isoformat()

        task = {
            "id": task_id,
            "description": desc,
            "status": self.status[0],
            "createdAt": timestamp,
            "updatedAt": timestamp
        }

        tasks.append(task)
        self.save_tasks(tasks)
        print(f"Task added (ID: {task_id})")

if __name__ == '__main__':
    TaskTracker().cmdloop()