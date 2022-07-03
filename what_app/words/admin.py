from django.contrib import admin
from .models import *


class WordAdmin(admin.ModelAdmin):
    all_profile = ProfileUser.objects.all().select_related()

    list_display = ('id', 'word', 'definition', 'example', 'user_id', 'get_user_id', 'word_add_date', 'like', 'dislike')
    list_display_links = ('id', 'word',)
    search_fields = ('word', 'user_id')
    list_filter = ('word', 'word_add_date', 'like', 'dislike',)
    readonly_fields = ('like', 'dislike', 'user_id',)
    fields = ('word', 'definition', 'example',)

    def get_user_id(self, obj):
        return obj.user_id.id

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user_id', None) is None:
            obj.user_id = ProfileUser.objects.get(name=User.objects.get(username=request.user))
        obj.save()

    get_user_id.short_description = "id пользователя"


class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reg',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('name', 'reg')
    fields = ('name', )


class ComplaintAdmin(admin.ModelAdmin):
    all_words = Word.objects.all().select_related()

    list_display = ('id', 'get_word_id', 'get_word', 'definition', 'example','complaint_add_date',)
    list_display_links = ('id', 'get_word_id', 'get_word',)
    search_fields = ('get_word',)
    fields = ('word_id', 'explanation',)

    def get_word_id(self, obj):
        return obj.word_id.id

    def get_word(self, obj):
        words = self.all_words.get(id=obj.word_id.id)
        return words.word

    def example(self, obj):
        return self.all_words.get(id=obj.word_id.id).example

    def definition(self, obj):
        return self.all_words.get(id=obj.word_id.id).definition

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user_id', None) is None:
            obj.user_id = ProfileUser.objects.get(name=User.objects.get(username=request.user))
        obj.save()

    get_word_id.short_description = "id слова"
    get_word.short_description = "слово"
    definition.short_description = "определение"
    example.short_description = "пример"


admin.site.register(ProfileUser, ProfileUserAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Word, WordAdmin)
