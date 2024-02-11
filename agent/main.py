import os

from openai import OpenAI

from agent.core import Core
from agent.implemented_parser import  parse_file_contents

core = Core()

text = """
```javascript
// models/task.js

const mongoose = require("mongoose");

const taskSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  status: {
    type: String,
    enum: ['pending', 'completed'],
    default: 'pending'
  },
  priority: {
    type: String,
    enum: ['low', 'medium', 'high'],
    default: 'medium'
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model("Task", taskSchema);
```

"""

if __name__ == "__main__":
    core.on_start()
    core.on_description()
    core.on_technologies()
    core.on_tasks()
    core.on_planing()
    core.on_project_structure()
    core.on_developing_tasks()
    core.on_summary()
    core.on_merge_updates()
    core.generate_bash()

    # Parse the text and print the result
    # files_array = parse_file_contents(text)
    # print(files_array['models/task.js'])
