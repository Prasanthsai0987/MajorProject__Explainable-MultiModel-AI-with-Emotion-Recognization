def generate_feedback(score):

    if score > 80:
        return "Excellent pronunciation but can still work on intonation and right you are in range of 80-100"

    elif score > 60:
        return "Good pronunciation but can improve clarity and right you are in range of 60-80"

    elif score > 40:
        return "Average pronunciation, practice vowels and right you are in range of 40-60"

    else:
        return "Pronunciation needs improvement focus on basic sounds and right you are in range of 10-40"
    
    
    