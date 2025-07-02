from django.contrib import admin
from . models import Question, FileUpload

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'category')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')

admin.site.register(Question, QuestionAdmin)
admin.site.register(FileUpload)
