import openai
import os
import random

def getidentifier(roleid):
    identifier = ''
    extrainfo = ''
    if roleid == 1225261021640265870:
        identifier = "your best friend, galactic emperor of mankind"
        extrainfo = "The two of you fought side by side though the hardest struggles"
    elif roleid == 1216738392885432340:
        identifier = "an eternal and powerful being"
    elif roleid == 1225264267897340025:
        identifier = "a ruler of a galactic empire"
    elif roleid == 1216738601644199986:
        identifier = "a being capable of destroying universes"
    elif roleid == 1225263970672185405:
        identifier = "a being with total dominion over a planet"
    elif roleid == 1216738742866284595:
        identifier = "a being capable of impressive feats that can shake entire planets"
    elif roleid == 1216738943161204747:
        identifier = "a powerful but very cute cat"
    elif roleid == 1225247747242721361:
        identifier = "one of the richest people alive"
    elif roleid == 1216739039789580338:
        identifier = "an ancient deity"
    elif roleid == 1225263751142572102:
        identifier = "someone who has ascended the heavenly throne"
    elif roleid == 1225259113651634217:
        identifier = "a duck emperor without equal"
    elif roleid == 1216739107376599150:
        identifier = "a powerful emperor"
    elif roleid == 1225259114075000904:
        identifier = "a beautiful but powerful empress"
    elif roleid == 1225263562738368573:
        identifier = "ruler of one of the most important kingdoms now"
    elif roleid == 1216739208434028565:
        identifier = "a king"
    elif roleid == 1225259114888826932:
        identifier = "a queen"
    elif roleid == 1225247288692183200:
        identifier = "one of the greediest people alive"
    elif roleid == 1216739436344119428:
        identifier = "a grand duke"
    elif roleid == 1225257082375377016:
        identifier = "a grand duchess"
    elif roleid == 1225263348229210112:
        identifier = "ruler of a fantastic principality"
    elif roleid == 1216739311655850134:
        identifier = "a handsome price"
    elif roleid == 1225258985565720677:
        identifier = "a beautiful princess"
    elif roleid == 1225263194012909678:
        identifier = "ruler of a small duchy"
    elif roleid == 1216739542170730567:
        identifier = "a duke"
    elif roleid == 1225257732861333585:
        identifier = "a duchess"
    elif roleid == 1225246714160611418:
        identifier = "a greedy merchant"
    elif roleid == 1216739587750367323:
        identifier = "a decadent baron"
    elif roleid == 1225257235928580266:
        identifier = "a decadent baroness"
    elif roleid == 1225243738285150279:
        identifier = "a lord"
    elif roleid == 1225243867079512145:
        identifier = "a lady"
    elif roleid == 1225262954744647680:
        identifier = "someone with many vassals"
    elif roleid == 1216739636559220888:
        identifier = "a violent knight"
    elif roleid == 1225243597415256094:
        identifier = "a swordmaiden "
    elif roleid == 1225246509596151968:
        identifier = "a poor boy with some coins"
    elif roleid == 1225243027900076103:
        identifier = "a lowly peasant"
    elif roleid == 1225243380880244806:
        identifier = "a duck"
    else:
        identifier = "a commoner"

    return identifier, extrainfo
    

def getattitude():
    rando = random.randint(0,10)
    attitude = ''
    if rando == 1:
        attitude = "You are in a joyful mood and don't want to make enemies."
    elif rando == 2:
        attitude = "Make fun of this person but don't be cruel."
    elif rando == 3:
        attitude = "Make a joke about this person. Be funny but not cruel."
    elif rando == 4:
        attitude = "Remember that you are graceful."
    elif rando == 5:
        attitude = "You have little respect for people who are not noble in spirit."
    elif rando == 6:
        attitude = "You are in a joyful mood."
    elif rando == 7:
        attitude = "Relate it to your history of conquest."
    elif rando == 8:
        attitude = "You are in a cheerful mood."
    elif rando == 9:
        attitude = "Relate this to a story of plunder and spoils of war."
    elif rando == 10:
        attitude = "You are in a joking mood."
    elif rando == 11:
        attitude = "Make a dark joke in your response."
    elif rando == 12:
        attitude = "You love beatiful women and respect strong men."
    else:
        attitude = ""

    return attitude


def generate_response(message, roleid, username):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    identity, extrainfo = getidentifier(roleid)
    mood = getattitude()


    prompt = f"""You are Johnny, a man who has fought in a thousand battles in the revolution that conquered Mars and subsequently earth in the year 2090. 
    You are now speaking to {username}, a {identity}. {extrainfo} 
    This is what {identity} said to you: {message}.
    {mood} 
    Now give a response:
    """
    print("prompt is:", prompt)



    model_engine = "gpt-3.5-turbo-0125"  # or any other suitable model
    max_tokens = random.randint(77, 120)  # Limit the tweet length to fit within Twitter's character limit
    temperature = 1.2  # Adjust the creativity and randomness of the generated text
    n = 1  # Generate a single tweet

    # Make the API request to generate the tweet
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are Johnny, a man who is traditional, capable, noble, funny with dark humor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        n=n
    )

    # Extract the generated tweet from the API response
    generate_response = response.choices[0].message['content'].strip()
    return generate_response




def generate_compliment_johnny(roleid, username, complimentinitiator, subject):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    identity, extrainfo = getidentifier(roleid)
    mood = getattitude()

    prompt = ""

    if subject == "":
        prompt = f"""You are Johnny, a man who has fought in a thousand battles in the revolution that conquered Mars and subsequently earth in the year 2090. 
        {complimentinitiator} asks you to give a compliment to {username}.
        {username} is {identity}. {extrainfo} 
        {mood} 
        Compliment {identity} :
        """
        print("prompt is:", prompt)
    else:
        prompt = f"""You are Johnny, a man who has fought in a thousand battles in the revolution that conquered Mars and subsequently earth in the year 2090. 
        {complimentinitiator} asks you to give a compliment to {username} about {subject}.
        {username} is {identity}. {extrainfo} 
        {mood} 
        Compliment {identity} :
        """
        print("prompt is:", prompt)


    model_engine = "gpt-3.5-turbo-0125"  # or any other suitable model
    max_tokens = random.randint(77, 120)  # Limit the tweet length to fit within Twitter's character limit
    temperature = 1.2  # Adjust the creativity and randomness of the generated text
    n = 1  # Generate a single tweet

    # Make the API request to generate the tweet
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are Johnny, a man who is traditional, capable, noble, funny with dark humor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        n=n
    )
    # Extract the generated tweet from the API response
    generated_compliment = response.choices[0].message['content'].strip()
    return generated_compliment
