from django.contrib import admin
from app.models import Profile, Question, Answer, LikeAnswer, LikeQuestion, Tag


class ProfileAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin):
    pass


class LikeQuestionAdmin(admin.ModelAdmin):
    pass


class LikeAnswerAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(LikeQuestion, LikeQuestionAdmin)
admin.site.register(LikeAnswer, LikeAnswerAdmin)
admin.site.register(Tag, TagAdmin)
