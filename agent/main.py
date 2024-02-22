import os
import re

import requests
from openai import OpenAI

from agent.JS_parser import parse_ast_conditionally, find_function_by_name, \
    find_arrow_function_by_name, find_event_listeners_by_variable, get_ast_request, \
    parse_required_modules, find_callback_bodies, find_express_app_variable, get_skeleton_method, count_event_listeners, \
    split_event_listeners, extract_function
from agent.core import Core
from agent.implemented_parser import parse_file_contents

core = Core()

code = """
    document.addEventListener('DOMContentLoaded', () => {
  // JavaScript for dynamic interactions will be written here
  // Function to Add a Task
  const addTask = () => {
    // Code to add a new task
    const taskName = taskInput.value;
        if (taskName) {
            const newTask = document.createElement("li");
            newTask.innerText = taskName;
            taskList.appendChild(newTask);
            taskInput.value = "";
            setupTaskActions(newTask);
        }
        
        taskItem.addEventListener("contextmenu", function (e) {
            e.preventDefault();
            taskItem.remove();
        });
  }
  
  

  // Function to Display Tasks
  const displayTasks = () => {
    // Code to display the list of tasks with filters and sorting
  }

  // Function to Mark Task as Complete
  const markAsComplete = (taskId) => {
    // Code to mark the task as complete
  }

  // Function to Delete a Task
  const deleteTask = (taskId) => {
    // Code to delete the task
  }

  // Function to Edit a Task
  const editTask = (taskId) => {
    // Code to edit the details of the task
  }

  // Function to Handle User Authentication
  const handleAuthentication = () => {
    // Code to implement user authentication
  }

  // Function to Set Due Dates and Reminders
  const setDueDateAndReminders = (taskId) => {
    // Code to set due dates for tasks
  }

  // Function to Prioritize Tasks
  const prioritizeTasks = () => {
    // Code to prioritize tasks using colors or sorting
  }

  // Add Event Listeners for the Above Functions
  // E.g., document.getElementById('addTaskBtn').addEventListener('click', addTask);
});
    """


code3 = """
    const taskInput = document.getElementById("taskInput");
    const addTaskBtn = document.getElementById("addTaskBtn");
    const taskList = document.getElementById("taskList");
    

    addTaskBtn.addEventListener("click", function () {
        const taskName = taskInput.value;
        if (taskName) {
            const newTask = document.createElement("li");
            newTask.innerText = taskName;
            taskList.appendChild(newTask);
            taskInput.value = "";
            setupTaskActions(newTask);
        }

        if (taskName) {
            const newTask = document.createElement("li");
            newTask.innerText = taskName;
            taskList.appendChild(newTask);
            taskInput.value = "";
            setupTaskActions(newTask);
        }

        taskItem.addEventListener("click", function () {
            taskItem.classList.toggle("completed");
            taskItem.classList.toggle("asdasd");
        });
    });

    function setupTaskActions(taskItem) {
        taskItem.addEventListener("click", function () {
            taskItem.classList.toggle("completed");
        });

        taskItem.addEventListener("contextmenu", function (e) {
            e.preventDefault();
            taskItem.remove();
        });
    }
"""

code4 = """ 
document.addEventListener("DOMContentLoaded", function () {
    const taskInput = document.getElementById("taskInput");
    const addTaskBtn = document.getElementById("addTaskBtn");
    const taskList = document.getElementById("taskList");
    const addTaskBtn2 = document.getElementById("taskListQ");
    
    const abc = () => {
        return 1 + 1; 
    };

    const dba = async () => {
        return 2 + 2; 
    };

    addTaskBtn2.addEventListener("click", async function () {
        // Your asynchronous code here
    });
    
    addTaskBtn.addEventListener("click", function () {
        const taskName = taskInput.value;
    });
    
    
    function setupTaskActions(taskItem) {
            taskItem.addEventListener("click", function () {
                taskItem.classList.toggle("completed");
            });
    
            taskItem.addEventListener("contextmenu", function (e) {
                e.preventDefault();
                taskItem.remove();
            });
    }
    
    async function displayTasks(sortByValue) {
        try {
            const response = await fetch(`/tasks?sortBy=${sortByValue}`); // Assuming the server supports sorting based on query parameters
            const data = await response.json();
            taskList.innerHTML = ""; // Clear the task list before displaying the new sorted tasks
            data.forEach((task) => {
                const newTask = document.createElement("li");
                newTask.innerText = task.name;
                if (task.status === "Completed") {
                    newTask.classList.add("completed");
                }
                taskList.appendChild(newTask);
                setupTaskActions(newTask);
            });
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    }
    
});

"""


server = """
 // app.js

const express = require("express");
const session = require("express-session");
const passport = require("passport");
const LocalStrategy = require("passport-local").Strategy;
const mongoose = require("mongoose");
const User = require("./models/user"); // User model

// Initialize Express app
const app = express();
app.use(express.json());

// Express session setup
app.use(session({
    secret: "secret",
    resave: false,
    saveUninitialized: false
}));

// Passport middleware setup
app.use(passport.initialize());
app.use(passport.session());

// Connect to MongoDB
mongoose.connect('mongodb://localhost/todoapp', { useNewUrlParser: true, useUnifiedTopology: true })
  
  
  
// Define User schema and model
// ... (User schema and model setup)

// Passport local strategy setup
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

// Authentication routes
 

app.post("/login", passport.authenticate("local"), (req, res) => {
    res.json({ message: "Login successful" });
});

app.get("/logout", (req, res) => {
    req.logout();
    res.json({ message: "Logged out" });
});

app.get("/user", (req, res) => {
    res.json(req.user);
});

// Protected route (example)
app.get("/tasks", (req, res) => {
    if (req.isAuthenticated()) {
        // Handle fetching tasks for authenticated user
        res.json({ message: "Tasks fetched for authenticated user" });
    } else {
        res.status(401).json({ message: "User not authenticated" });
    }
});

// ... Additional routes for managing tasks

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});
"""

code2_1 = """
// script.js

document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('taskForm');
    const taskInput = document.getElementById('taskInput');
    const taskList = document.getElementById('taskList');
    
    taskList.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            toggleTaskCompletion(event.target); // Call function to toggle task completion
        }
    });

    taskForm.addEventListener('submit', function(event) {
        event.preventDefault();
        if (taskInput.value) {
            addNewTask(taskInput.value); // Call function to add new task
            taskInput.value = "";
        }
    });

    taskList.addEventListener('contextmenu', function(event) {
        event.preventDefault();
        if (event.target.tagName === 'LI') {
            deleteTask(event.target); // Call function to delete task
        }
    });

    // Function to add new task
    function addNewTask(taskName) {
        const newTask = document.createElement('li');
        newTask.innerText = taskName;
        taskList.appendChild(newTask);
    }

    // Function to toggle task completion
    function toggleTaskCompletion(task) {
        task.classList.toggle('completed');
    }

    // Function to delete task
    function deleteTask(task) {
        task.remove();
    }
}); 
"""

server2_1 = """
// server.js

const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost/todoApp', { useNewUrlParser: true, useUnifiedTopology: true });

// Define task schema
const TaskSchema = new mongoose.Schema({
    name: String,
    completed: { type: Boolean, default: false }
});
const Task = mongoose.model('Task', TaskSchema);

// Middleware
app.use(bodyParser.json());

// API endpoints
app.get('/tasks', async (req, res) => {
    try {
        const tasks = await Task.find();
        res.json(tasks);
    } catch (error) {
        res.status(500).send(error.message);
    }
});

app.post('/tasks', async (req, res) => {
    const task = new Task({ name: req.body.name });
    try {
        const newTask = await task.save();
        res.json(newTask);
    } catch (error) {
        res.status(400).send(error.message);
    }
});

app.put('/tasks/:id', async (req, res) => {
    try {
        const updatedTask = await Task.findByIdAndUpdate(req.params.id, { completed: req.body.completed }, { new: true });
        res.json(updatedTask);
    } catch (error) {
        res.status(400).send(error.message);
    }
});

app.delete('/tasks/:id', async (req, res) => {
    try {
        await Task.findByIdAndDelete(req.params.id);
        res.send('Task deleted successfully');
    } catch (error) {
        res.status(400).send(error.message);
    }
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 
"""

def langchain():

    from langchain_community.llms import OpenAI
    import os
    os.environ["OPENAI_API_KEY"] = "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"

    llm = OpenAI(model_name="gpt-3.5-turbo-1106")

    with open("blanks/user_project_details.blank", "r") as file:
        project_details = file.read().strip()
    project_descr = project_details

    with open("prompts/technologies.prompt", "r") as file:
        tech_prompt = file.read().strip()

    final_prompt = (tech_prompt
                    .replace('{{ name }}', "todo")
                    .replace('{{ project_details }}', project_descr))

    print(llm(final_prompt))

if __name__ == "__main__":

    # langchain()

    print("START...\n\n")
    core.on_start()

    print("Description...\n\n")
    core.on_description()

    print("Technologies...\n\n")
    core.on_technologies()

    print("Tasks...\n\n")
    core.on_tasks()

    print("Planing...\n\n")
    core.on_planing()

    print("Project Structure...\n\n")
    core.on_project_structure()

    print("Implementing Tasks..\n\n")
    core.on_developing_tasks()

    print("Merge Files...\n\n")
    core.on_merge_files()
    #
    # print("Modularity Files HTML JS...\n\n")
    # core.on_modularity_html_js()
    #
    # # print("Modularity...\n\n")
    # # core.on_check_modularity()
    #
    # print("Summary...\n\n")
    # core.on_summary()
    #
    print("Generate Build File (build.sh)...\n\n")
    core.generate_bash()




    # ast = get_ast_request(server2_1)
    # defined_v_f = parse_required_modules(ast)
    # print(defined_v_f)
    #
    # variable_name = find_express_app_variable(server2_1)
    # print(variable_name)
    #
    # callback_bodies = find_callback_bodies(server2_1, variable_name)
    # for i, body in enumerate(callback_bodies):
    #     replacer = get_skeleton_method(body)
    #     if replacer is not None:
    #        server2_1 = server2_1.replace(body,replacer)
    #
    # print(server2_1)

    # ast = get_ast_request(code2_1)
    # defined_v_f = parse_ast_conditionally(ast)
    # print(defined_v_f)
    #
    # for key in defined_v_f.keys():
    #     if 'document' in defined_v_f[key]:
    #         defined_v_f[key].remove('document')
    #
    # for function in defined_v_f["functions"]:
    #     fun = find_function_by_name(code2_1, function)
    #     replacer = get_skeleton_method(fun)
    #     if replacer is not None:
    #         code2_1 = code2_1.replace(fun,replacer)
    #
    # for function in defined_v_f["arrow_functions"]:
    #     fun = find_arrow_function_by_name(code2_1, function)
    #     replacer = get_skeleton_method(fun)
    #     if replacer is not None:
    #         code2_1 = code2_1.replace(fun,replacer)
    #
    #
    # for function in defined_v_f["callbacks"]:
    #     fun = find_event_listeners_by_variable(code2_1, function)
    #
    #     if count_event_listeners(fun) > 1:
    #         event_listeners = split_event_listeners(fun, function)
    #
    #         for event in event_listeners:
    #             replacer = get_skeleton_method(event)
    #             if replacer is not None:
    #                 code2_1 = code2_1.replace(event, replacer)
    #     else:
    #         replacer = get_skeleton_method(fun)
    #         if replacer is not None:
    #             code2_1 = code2_1.replace(fun,replacer)
    #
    # print(code2_1)

    # function_start = "taskList.addEventListener('click', function(event) {"
    # extracted_function = extract_function(code2_1, function_start)
    #
    # # Display the extracted function
    # print(extracted_function)