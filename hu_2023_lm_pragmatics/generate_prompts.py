import random
import sys
import jsonlines
import pandas as pd
from tqdm import tqdm
sys.path.append("..")

json_out = []
CHARACTER_LIMIT = 32000

###Deceits

df1 = pd.read_csv("Data/Human_Deceits.csv")
df2 = pd.read_csv("Data/Deceits_prompts_seed0_examples0.csv")

# general task instructions
task = (
    "{text} {response}\n\n"
)
#go over participants
for participant in tqdm(df1.pKey.unique()):
    # create a future json entry for the participant
    par_dict = {"text": "", "experiment": 'hu2023lm-pragmatics/Human_Deceits.csv', "participant": str(participant)}
    #reindex and drop the old index
    par_df = df1[df1.pKey == participant].reset_index(drop=True)
    #Correctness list
    correct_list=[]
    # iterate over trials
    for _, trial in par_df.iterrows():

        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])
        #get the list of how answers were scrumbled
        scrumbled_list = eval(df2.loc[trial["itemNum"]-1, "randomized_option_order"])
        #get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        #get the instructions
        text = df2.loc[trial["itemNum"]-1, "prompt"]

        #options finding
        one_idx=text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        answer_idx = text.find("Answer:")
        options=[text[(one_idx+3):two_idx], text[(two_idx+3):three_idx], text[(three_idx+3):four_idx], text[(four_idx+3):answer_idx]]

        #get the actual response
        response = options[response_idx]

        #shuffle options
        random.shuffle(options)

        # response in the prompt:
        resp_prompt = options.index(response)+1

        #get the new prompt
        new_text = text[:one_idx]+"1) "+options[0]+"2) "+options[1]+"3) "+options[2]+"4) "+options[3]+"Answer:"

        #fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"
        correct_list.append(trial["Correct"])

    #append list of correct responses
    par_dict["Correctness"] = correct_list
    # check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    json_out.append(par_dict)


###Maxims

df1 = pd.read_csv("Data/Human_Maxims.csv")
df2 = pd.read_csv("Data/Maxims_prompts_seed0_examples0.csv")

# general task instructions
task = (
    "{text} {response}\n\n"
)
#go over participants
for participant in tqdm(df1.pKey.unique()):
    # create a future json entry for the participant
    par_dict = {"text": "", "experiment": 'hu2023lm-pragmatics/Maxims.csv', "participant": str(participant)}
    #reindex and drop the old index
    par_df = df1[df1.pKey == participant].reset_index(drop=True)
    #Correctness lis
    correct_list=[]
    # iterate over trials
    for _, trial in par_df.iterrows():

        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])

        #omit the discrepancy (no prompt number 13) in data
        itemNum = trial["itemNum"]
        if itemNum < 13:
            index = itemNum - 1
        elif itemNum > 13:
            index = itemNum - 2
        else:
            continue

        #get the list of how answers were scrumbled
        scrumbled_list = eval(df2.loc[index, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df2.loc[index, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # response in the prompt:
        resp_prompt = options.index(response) + 1

        # get the new prompt
        new_text = text[:one_idx] + "1) " + options[0] + "2) " + options[1] + "3) " + options[2] + "4) " + options[3] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"
        #add correctness
        correct_list.append(trial["Correct"])

    # append list of correct responses
    par_dict["Correctness"] = correct_list
    # check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    json_out.append(par_dict)


###Humour

df1 = pd.read_csv("Data/Human_Humour.csv")
df2 = pd.read_csv("Data/Humour_prompts_seed0_examples0.csv")

# general task instructions
task = (
    "{text} {response}\n\n"
)
#go over participants
for participant in tqdm(df1.pKey.unique()):
    # create a future json entry for the participant
    par_dict = {"text": "", "experiment": 'hu2023lm-pragmatics/Humour.csv', "participant": str(participant)}
    #reindex and drop the old index
    par_df = df1[df1.pKey == participant].reset_index(drop=True)
    #Correctness list
    correct_list=[]
    # iterate over trials
    for _, trial in par_df.iterrows():

        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])

        #get the list of how answers were scrumbled
        scrumbled_list = eval(df2.loc[trial["itemNum"]-1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df2.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        five_idx = text.find("5)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):five_idx], text[(five_idx+3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # response in the prompt:
        resp_prompt = options.index(response) + 1

        # get the new prompt
        new_text = text[:one_idx] + "1) " + options[0] + "2) " + options[1] + "3) " + options[2] + "4) " + options[
            3] + "5) "+ options[4] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"
        #append correctness
        correct_list.append(trial["Correct"])

    # append list of correct responses
    par_dict["Correctness"] = correct_list
    # check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    json_out.append(par_dict)


###Coherence

df1 = pd.read_csv("Data/Human_CoherenceInference.csv")
df2 = pd.read_csv("Data/CoherenceInference_prompts_seed0_examples0.csv")

# general task instructions
task = (
    "{text} {response}\n\n"
)
#go over participants
for participant in tqdm(df1.pKey.unique()):
    # create a future json entry for the participant
    par_dict = {"text": "", "experiment": 'hu2023lm-pragmatics/CoherenceInference.csv', "participant": str(participant)}
    #reindex and drop the old index
    par_df = df1[df1.pKey == participant].reset_index(drop=True)
    #Correctness list
    correct_list=[]
    # iterate over trials
    for _, trial in par_df.iterrows():

        # get the response Coherent|Incoherent
        coherent_response = trial["OptionChosen"]

        # covert "Coherent" to 1 and "Incoherent" to 2
        if coherent_response == "Coherent":
            index = 1
        else:
            index = 2

        #get the list of how answers were scrumbled
        scrumbled_list = eval(df2.loc[trial["itemNum"]-1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(index)
        # get the instructions
        text = df2.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # response in the prompt:
        resp_prompt = options.index(response) + 1

        # get the new prompt
        new_text = text[:one_idx] + "1) " + options[0] + "2) " + options[1] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instuction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instuction + "\n"

        #append the correctness
        correct_list.append(trial["Correct"])

    # append list of correct responses
    par_dict["Correctness"] = correct_list

    # check that the prompt is not too long
    assert (
        len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    json_out.append(par_dict)



###Indirect Speech

df1 = pd.read_csv("Data/Human_IndirectSpeech.csv")
df2 = pd.read_csv("Data/IndirectSpeech_prompts_seed0_examples0.csv")
# go over participants
for participant in tqdm(df1.pKey.unique()):
    # create a future json entry for the participant
    par_dict = {"text": "", "experiment": 'hu2023lm-pragmatics/Human_IndirectSpeech.csv',
                "participant": str(participant)}
    # reindex and drop the old index
    par_df = df1[df1.pKey == participant].reset_index(drop=True)
    # Correctness list
    correct_list = []
    # iterate over trials
    for _, trial in par_df.iterrows():
        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])
        # get the list of how answers were scrumbled
        scrumbled_list = eval(df2.loc[trial["itemNum"] - 1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df2.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # response in the prompt:
        resp_prompt = options.index(response) + 1

        # get the new prompt
        new_text = text[:one_idx] + "1) " + options[0] + "2) " + options[1] + "3) " + options[2] + "4) " + options[
            3] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"

        # append the correctness
        correct_list.append(trial["Correct"])

    # append list of correct responses
    par_dict["Correctness"] = correct_list
    # check that the prompt is not too long
    assert (
            len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    json_out.append(par_dict)

###Metaphor

df1 = pd.read_csv("Data/Human_Metaphor.csv")
df2 = pd.read_csv("Data/Metaphor_prompts_seed0_examples0.csv")
# go over participants
for participant in tqdm(df1.pKey.unique()):
    # create a future json entry for the participant
    par_dict = {"text": "", "experiment": 'hu2023lm-pragmatics/Human_Metaphor.csv', "participant": str(participant)}
    # reindex and drop the old index
    par_df = df1[df1.pKey == participant].reset_index(drop=True)
    # Correctness list
    correct_list = []
    # iterate over trials
    for _, trial in par_df.iterrows():
        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])
        # get the list of how answers were scrumbled
        scrumbled_list = eval(df2.loc[trial["itemNum"] - 1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df2.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        five_idx = text.find("5)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):five_idx], text[(five_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # response in the prompt:
        resp_prompt = options.index(response) + 1

        # get the new prompt
        new_text = text[:one_idx] + "1) " + options[0] + "2) " + options[1] + "3) " + options[2] + "4) " + options[
            3] + "5) " + options[4] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"

        # append the correctness
        correct_list.append(trial["Correct"])

    # append list of correct responses
    par_dict["Correctness"] = correct_list
    #check that the prompt is not too long
    assert (
            len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    json_out.append(par_dict)

###Irony

df1 = pd.read_csv("Data/Human_Irony.csv")
df2 = pd.read_csv("Data/Irony_prompts_seed0_examples0.csv")
# go over participants
for participant in tqdm(df1.pKey.unique()):
    # create a future json entry for the participant
    par_dict = {"text": "", "experiment": 'hu2023lm-pragmatics/Human_Irony.csv', "participant": str(participant)}
    # reindex and drop the old index
    par_df = df1[df1.pKey == participant].reset_index(drop=True)
    # Correctness list
    correct_list = []
    # iterate over trials
    for _, trial in par_df.iterrows():
        # get the scrumbled response as number (e.g. Answer3 -> 3)
        scrumbled_response = int(trial["OptionChosen"][-1])
        # get the list of how answers were scrumbled
        scrumbled_list = eval(df2.loc[trial["itemNum"] - 1, "randomized_option_order"])
        # get the response index in the prompts seed 0
        response_idx = scrumbled_list.index(scrumbled_response)
        # get the instructions
        text = df2.loc[trial["itemNum"] - 1, "prompt"]

        # options finding
        one_idx = text.find("1)")
        two_idx = text.find("2)")
        three_idx = text.find("3)")
        four_idx = text.find("4)")
        answer_idx = text.find("Answer:")
        options = [text[(one_idx + 3):two_idx], text[(two_idx + 3):three_idx], text[(three_idx + 3):four_idx],
                   text[(four_idx + 3):answer_idx]]

        # get the actual response
        response = options[response_idx]

        # shuffle options
        random.shuffle(options)

        # response in the prompt:
        resp_prompt = options.index(response) + 1

        # get the new prompt
        new_text = text[:one_idx] + "1) " + options[0] + "2) " + options[1] + "3) " + options[2] + "4) " + options[
            3] + "Answer:"

        # fill the parameters to the trial outputs
        trial_instruction = task.format(
            text=new_text,
            response=f"<<{resp_prompt}>>"
        )
        # append trial prompt to participant's recording
        par_dict["text"] += trial_instruction + "\n"

        # append the correctness
        correct_list.append(trial["Correct"])

    # append list of correct responses
    par_dict["Correctness"] = correct_list
    # check that the prompt is not too long
    assert (
            len(par_dict["text"]) < CHARACTER_LIMIT
    ), f"Participant {participant} has too many characters: ({len(par_dict['text'])})"

    json_out.append(par_dict)

#write to the jsonl file
with jsonlines.open("prompts.jsonl", "w") as writer:
    writer.write_all(json_out)






