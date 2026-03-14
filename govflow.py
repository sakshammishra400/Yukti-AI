from agents import planner_agent, document_agent, form_agent, validation_agent

def run():

    print("\n========================")
    print("      GovFlow AI")
    print("========================\n")

    service = input("What government service do you need?\n> ")

    print("\n--- Planner Agent ---\n")
    print(planner_agent(service))

    print("\n--- Document Agent ---\n")
    print(document_agent(service))

    print("\n--- Form Agent ---\n")
    print(form_agent(service))

    print("\n--- Validation Agent ---\n")
    print(validation_agent(service))


if __name__ == "__main__":
    run()