
def clean(txt_data):
    for index, txt in enumerate(txt_data):
        data = " ".join(txt['ocr'].split())
        txt_data[index]['ocr'] = data

    return txt_data
