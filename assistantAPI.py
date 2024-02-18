import time
import openai
from openai import OpenAI
client = openai.Client(api_key="")

# Step 1: Get user input
print("Welcome to the playlist generator! Please tell me what you would like to base the playlist on. You can choose from artist, genre, songs, albums, or suggest some options.")
user_reply = input("Please type your choice: ")
print("Thanks, and how many songs would you like to generate and would you like me to stay close to your original choices or be more creative with my selection?")
user_reply2 = input("Please type the number of songs you would like and then 1 to 10 for Close to Creative: ")

lv_prompt1 = user_reply + " * " + user_reply2 + " (number of songs and then 1 to 10 for Close to Creative Respectively): "
my_assistant = client.beta.assistants.retrieve("asst_dGA1kf4caeNl5VPFd9MJPzUm")
#print(my_assistant)

my_thread = client.beta.threads.create()

my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role="user",
  content=lv_prompt1,
)

my_run = client.beta.threads.runs.create(
  thread_id=my_thread.id,
  assistant_id=my_assistant.id
)
while my_run.status in ["queued", "in_progress"]:
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=my_thread.id,
        run_id=my_run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")
    if keep_retrieving_run.status == "completed":
            print("\n")

            # Step 6: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
            )

            print("------------------------------------------------------------ \n")

            print(f"User: {my_thread_message.content[0].text.value}")
            print(f"Assistant: {all_messages.data[0].content[0].text.value}")
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=my_thread.id,
        run_id=my_run.id
)

    if keep_retrieving_run.status == "requires_action":
        all_messages = client.beta.threads.messages.list(thread_id=my_thread.id)
        print("------------------------------------------------------------ \n")
        print(f"User: {my_thread_message.content[0].text.value}")
        print(f"Assistant: {all_messages.data[0].content[0].text.value}") 
        print("Action Required")
        user_reply5 = input("Please enter your response: ")
        my_thread_message = client.beta.threads.messages.create(
            thread_id=my_thread.id,
            role="user",
            content=user_reply5,
        )
    #elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
        #pass
    else:
        print(f"Run status: {keep_retrieving_run.status}")
    break
all_messages = client.beta.threads.messages.list(
    thread_id=my_thread.id
)
#List run steps
run_steps = client.beta.threads.runs.steps.list(
    thread_id=my_thread.id,
    run_id=my_run.id
)
print("******************1. Printing Run Steps List")
print(run_steps)

#Retrieve a run
run = client.beta.threads.runs.retrieve(
  thread_id=my_thread.id,
  run_id=my_run.id,
)
print("******************2. Printing Run")
print(run)

#Retrieve a run step

#submit tool outputs to run
tool_run = client.beta.threads.runs.submit_tool_outputs(
  thread_id=my_thread.id,
  run_id=my_run.id,
  tool_outputs=[
    {
      "tool_call_id": "call_abc123",
      "output": "28C"
    }
  ]
)
print("4. submitted tool to run")
print(run)
#create
user_reply3 = input("Are you happy with the recommendation? please type yes or no: ")
if user_reply3 == "yes":
    print("Thank you for using our service!")
elif user_reply3 == "no":
    print("Please tell us what you would like to change about the recommendation")
    user_reply4 = input("Please type the name of the song you would like to change: ")
    user_reply5 = input("Please type the name of the song you would like to replace it with: ")
    print("Ok, lets put our foot on the amp and give that another go! Thank you for using our service!")
print("------------------------------------------------------------ \n")

print(f"User: {my_thread_message.content[0].text.value}")
print(f"Assistant: {all_messages.data[0].content[0].text.value}")

# Send a new user message to the assistant
new_user_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role="user",
  content="I like rock music and my favorite band is The Beatles.",
)

# Run the assistant again
my_run = client.beta.threads.runs.create(
  thread_id=my_thread.id,
  assistant_id=my_assistant.id
)