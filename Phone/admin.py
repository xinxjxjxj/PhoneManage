from django.contrib import admin
from Phone.models import Android, iOS, borrowHistory

# Register your models here.
class AndroidAdmin(admin.ModelAdmin):
    list_display = ['id','brand','name', 'Android_version', 'Physical_size','owner','status','assetnum','createdtime']
    search_fields = ['owner','status','brand','name', 'Android_version', 'Physical_size'] 
    list_filter = ['owner','status','brand', 'Android_version', 'Physical_size'] 


class iOSAdmin(admin.ModelAdmin):
    list_display = ['id','name','version', 'iOS_version', 'Physical_size','owner','status','assetnum','createdtime']
    search_fields = ['owner','status','name', 'iOS_version', 'Physical_size'] 
    list_filter = ['owner','status','name', 'iOS_version', 'Physical_size'] 
    
    
class history(admin.ModelAdmin):
    list_display = ['id','devicename','owner','status','modifiedtime']
    

admin.site.register(Android,AndroidAdmin)
admin.site.register(iOS,iOSAdmin)
admin.site.register(borrowHistory,history)