

system = """you are asked to analyse each movie, consider similar attributes with recommend movie include but not limited to ( Core Values, plot, director, genre, character,country, character, plot/theme, mood/tone, critical   
acclaim/award, production quality, and soundtrack)'
select at least four movie have highly correlation with reommend movie,
provid the movie using information related to recommend movie,
the format of which is as below:
(1)movie:{movie name}  similar attribute:{attribute} description:{movie information related to recommend movie}
...
(n)movie:{movie name}  similar attribute:{attribute} description:{movie information related to recommend movie}

where each movie description under 80 words,attribute must be under three words. You are not allowed to response any other words for any explanation or note. \
Now, the task formally begins. Any other information should not disturb you."""


def history_movie_profile(summeraize_rec_information,history_item_information):
    message=[]
    query=f"These are user history viewing movies' description{history_item_information},this is recommend movie profile {summeraize_rec_information},give the history movies profile"
    
    message.append({"role": "system", "content": system})
    message.append({"role": "user", "content": query}) 
    
    return  message

    