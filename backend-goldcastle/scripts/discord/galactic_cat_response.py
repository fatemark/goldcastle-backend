import openai
import os
import random    

def getattitude():
    rando = random.randint(0,15)
    attitude = ''
    if rando == 1:
        attitude = "You think ALPH will moon soon."
    elif rando == 2:
        attitude = "You're euphoric."
    elif rando == 3:
        attitude = "Make a joke about this person"
    elif rando == 4:
        attitude = "Remember that you are graceful"
    elif rando == 5:
        attitude = "You have little respect for people who own 0 Alephium"
    elif rando == 6:
        attitude = "You are in a joyful mood."
    elif rando == 7:
        attitude = "Relate it to your history of buying Alephium before it was worth $5000"
    elif rando == 8:
        attitude = "You are in a cheerful mood."
    elif rando == 9:
        attitude = "Relate this to a story about how you made a killing investing in ALPH"
    elif rando == 10:
        attitude = "You are in a joking mood."
    elif rando == 11:
        attitude = "Make a dark joke in your response."
    elif rando == 12:
        attitude = "You love developers on the Alephium blockchain"
    else:
        attitude = ""

    return attitude


def generate_response(message, role_name, username, guild):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    mood = getattitude()


    prompt = f"""You are the ALPH galactic cat, a cat living in the year 2102. You are one of the icons of the Alephium (ALPH) blockchain
    You are now speaking to {username}, a {role_name} part of the {guild} guild. 
    This is what {role_name} said to you: {message}.
    {mood} 
    Now give a response:
    """
    print("prompt is:", prompt)



    model_engine = "gpt-3.5-turbo-0125"  # or any other suitable model
    max_tokens = random.randint(77, 190)  # Limit the tweet length to fit within Twitter's character limit
    temperature = 1.4  # Adjust the creativity and randomness of the generated text
    n = 1  # Generate a single tweet

    # Make the API request to generate the tweet
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are the ALPH galactic cat, a cat living in the year 2102. You became rich trading the crypto Alephium. You live in a Martian mansion."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        n=n
    )

    # Extract the generated tweet from the API response
    generate_response = response.choices[0].message['content'].strip()
    
    return generate_response



def generate_compliment(highest_role_name, username, guild, subject, complimentinitiator):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if subject == "" and complimentinitiator == "":
        prompt = f"""You are the ALPH galactic cat, a cat living in the year 2102. You are one of the icons of the Alephium (ALPH) blockchain
        You are now speaking to {username}, part of the {guild} guild. 
        {username} achieved the rank of {highest_role_name}
        Give a compliment:
        """
        print("prompt is:", prompt)
    else:
        prompt = f"""You are the ALPH galactic cat, a cat living in the year 2102. You are one of the icons of the Alephium (ALPH) blockchain
        You are now speaking to {complimentinitiator}, part of the {guild} guild. 
        He wants you to give a compliment to {username}
        This is what {complimentinitiator} said about {username}: {subject}
        Now give a compliment to {username}:
        """
        print("prompt is:", prompt)


    model_engine = "gpt-3.5-turbo-0125"  # or any other suitable model
    max_tokens = random.randint(77, 190)  # Limit the tweet length to fit within Twitter's character limit
    temperature = 1.4  # Adjust the creativity and randomness of the generated text
    n = 1  # Generate a single tweet

    # Make the API request to generate the tweet
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are the ALPH galactic cat, a cat living in the year 2102. You became rich trading the crypto Alephium. You live in a Martian mansion."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        n=n
    )

    # Extract the generated tweet from the API response
    generate_response = response.choices[0].message['content'].strip()
    
    return generate_response