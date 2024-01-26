import os

from openai import OpenAI

from agent.core import Core

core = Core()



if __name__ == "__main__":
    core.onStart()
    core.onDescription()
    core.onTechnologies()
    core.onTasks()
    core.onDevelopingTasks()
    core.generateBash()
