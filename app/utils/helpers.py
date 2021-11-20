
def clean(txt_data):
    for index, txt in enumerate(txt_data):
        data = " ".join(txt['text'].split())
        txt_data[index]['text'] = data
    
    return txt_data
