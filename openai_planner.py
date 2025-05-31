from openai import OpenAI
import os
def planner_trip(destination, start_date,end_date):
    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
    response = client.chat.completions.create(
    model="gpt-4o",  # Or "gpt-4-1106-preview", etc.
    messages=[
        {"role": "system", "content": "You are a travel planner assistant."},
        {"role": "user", "content": f"Make me a travel plan to {destination} . I am leaving on {start_date} and coming back on {end_date} . include general and seasonal information also include the per day schedule "}
    ]
)
    return(response.choices[0].message.content)


