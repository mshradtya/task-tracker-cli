import cmd
import json
import os
from datetime import datetime
import re

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
        
    def get_task(self, id):
        tasks = self.get_tasks()
        task = list(filter(lambda x: x['id'] == id, tasks))
        if len(task) == 0:
            return None
        return task[0]
    
    def get_next_id(self, tasks):
        return max([task["id"] for task in tasks], default=0) + 1
    
    def to_int(self, id):
        try:
            return int(id.strip())
        except:
            return None

    def save_tasks(self, tasks):
        with open(self.file_name, 'w') as f:
            json.dump({"tasks": tasks}, f, indent=4)
        
    def extract_update_info(self, s):
        match = re.match(r'^\s*(\d+)\s+(.*)', s)
        if match:
            id = int(match.group(1))
            desc = match.group(2).strip()
            return id, desc
        return None, None
    
    def update_task(self, id, desc):
        tasks = self.get_tasks()
        timestamp = datetime.now().isoformat()
        for t in tasks:
            if t['id'] == id:
                t['description'] = desc
                t['updatedAt'] = timestamp
                break
        return tasks
    
    def delete_task(self, id):
        tasks = self.get_tasks()
        updated = list(filter(lambda t: t['id'] != id, tasks))
        return updated
    
    def do_update(self, arg):
        id, desc = self.extract_update_info(arg)
        if id == None or desc == None:
            print('Enter valid ID and description')
            return
        task = self.get_task(id)
        if task == None:
            print(f"Task with ID {id} doesn't exist")
            return
        updated_tasks = self.update_task(id, desc)
        self.save_tasks(updated_tasks)
        print(f"Task updated (ID: {id})")

    def do_delete(self, arg):
        id = self.to_int(arg)
        if id is None:
            print('Enter valid task ID')
            return
        task = self.get_task(id)
        if task == None:
            print(f"Task with ID {id} doesn't exist")
            return
        updated_tasks = self.delete_task(id)
        self.save_tasks(updated_tasks)
        print(f"Task deleted (ID: {id})")

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

    def do_quit(self, arg):
        return True

if __name__ == '__main__':
    TaskTracker().cmdloop()