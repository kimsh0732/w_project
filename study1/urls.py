"""study1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# http://localhost:8000 요청의 시작점
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
#    path('admin/', admin.site.urls),
#     http://localhost:8000/member
     path("member/",include('member.urls')),
#     http://localhost:8000/board
     path("board/",include('board.urls')) #
]
#파일 업로드를 위한 설정
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
