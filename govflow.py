from agents import planner_agent, document_agent, form_agent, validation_agent

def run_agent(user_request):

    plan = planner_agent(user_request)
    docs = document_agent(plan)
    form = form_agent(plan)
    validation = validation_agent(form)

    result = f"""
Plan:
{plan}

Required Documents:
{docs}

Form Filled:
{form}

Validation:
{validation}
"""

    return result