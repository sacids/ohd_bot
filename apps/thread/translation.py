from modeltranslation.translator import translator, TranslationOptions
from .models import Thread, SubThread


class ThreadTranslationOptions(TranslationOptions):
    fields = ('title',)


class SubThreadTransalationOptions(TranslationOptions):
    fields = ('title', 'description',)    


translator.register(Thread, ThreadTranslationOptions)    
translator.register(SubThread, SubThreadTransalationOptions)   