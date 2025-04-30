from django import template

register = template.Library()

@register.filter
def mood_emoji(value):
    emojis = {
        1 : '🤩' ,
        2 : '😃' ,
        3 : '😊' ,
        4 : '🤭' ,
        5 : '🥰' ,
        6 : '🍵' ,
        7 : '😖' ,
        8 : '😢' ,
        9 : '😕' ,
        10: '😭' ,
        11: '😠' ,        
    }
    return emojis.get(value, '❓')  # default if mood not found