# Task Tracker CLI

A simple command-line task tracker built with Python. 1/22 project of roadmap.sh/backend.

## Features

- Add new tasks
- Update task descriptions
- Delete tasks
- Mark tasks as in-progress or done
- List all tasks or filter by status
- View created and updated timestamps

## Requirements

- Python 3.10 or higher

## How to Run

```bash
python app.py
```

## Commands

```
add <description>            # Add a new task
update <id> <description>    # Update an existing task
delete <id>                  # Delete a task by ID
progress <id>                # Mark task as in-progress
done <id>                    # Mark task as done
list                         # List all tasks
list todo                    # List tasks with status 'todo'
list progress                # List tasks with status 'in-progress'
list done                    # List tasks with status 'done'
quit                         # Exit the program
```

## Example

```bash
add Finish backend project
progress 1
update 1 Finish backend project and review code
done 1
list done
```
