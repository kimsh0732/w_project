from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Member
from django.contrib import auth
#member/views.py
# Create your views here.
# View(Controller 역할) 담당 파일. 

def login(request) :
    if request.method != 'POST' :
       return render(request,'member/login.html')  #render : forward
    else :
        #파라미터값 저장
        id1 = request.POST["id"]   #id 파라미터값
        pass1 = request.POST["pass"] #pass 파라미터값
        try :
            #id=id1인 정보를 db table에서 조회.
            #id1에 해당하는 레코드가 없는 경우 예외발생
           member = Member.objects.get(id=id1) #id값이 id1인 데이터를 조회
           if member.pass1 == pass1 : #비밀번호 일치
             #request.session : session 객체
              session_id = request.session.session_key #session id값 조회
              #세션객체에 login 속성 등록. 로그인 정보 세션에 등록
              request.session['login'] = id1  
              return HttpResponseRedirect("../main") 
           else :  #비밀번호 불일치
              context = {"msg":"비밀번호가 틀립니다.","url":"../login/"}
              return render(request,'alert.html',context)
        except :
           context = {"msg":"아이디를 확인하세요."}
           return render(request,'member/login.html',context)
            
    
#http://localhost:8000/member/join
def join(request) :
    if request.method != 'POST' :
       return render(request,'member/join.html')
    else :  #method=POST 
       #회원가입 
       #request.POST['id'] : POST 방식으로 id파라미터값
       #member : 화면에서 등록된 회원정보 내용 저장
       member = Member(id=request.POST['id'],\
                       pass1=request.POST['pass'],\
                       name=request.POST['name'],\
                       gender=request.POST['gender'],\
                       tel=request.POST['tel'],\
                       email=request.POST['email'],\
                       picture=request.POST['picture'])
       member.save()  #database에 저장.
       return HttpResponseRedirect("../login/") #redirect
   
def main(request) :
       return render(request,'member/main.html')  #render : forward


def logout(request) :
    auth.logout(request)  #세션종료 
    return HttpResponseRedirect("../login")

#  info/<str:id>/ => info 요청값 이후에값은 id 문자열값 전달
def info(request,id) :   #id=admin
   try :
       login = request.session["login"] #로그인 정보 데이터
   except : #로그인이 안된경우 예외 발생
       login = ""
       
   if login != "" :  #로그인 
       if login == id or login == 'admin' :
           member = Member.objects.get(id=id) #id에 해당하는 db정보 저장
           return render(request,"member/info.html",{"mem":member})
       else : #관리자가 아니 사용자가 다른정보 조회.
           context = {"msg":"본인정보만 조회 가능","url":"../../main"}
           return render(request,"alert.html",context)
   else :  #로그아웃
      context = {"msg":"로그인 하세요","url":"../../login"}
      return render(request,"alert.html",context)

def update(request,id):  #id : apple 아이디정보
    try :
        login = request.session["login"]  #세션정보. 로그인 정보 
    except :
        context = {"msg": "로그인 하세요.", "url": "../../login/"}
        return render(request, 'alert.html', context)
        
    if login == id or login == 'admin' :
        return update_rtn(request,id)
    else :
       context = {"msg": "본인 정보만 수정가능합니다.", "url": "../../main/"}
       return render(request, 'alert.html', context)

def update_rtn(request,id) :
    if request.method != "POST" :
       member = Member.objects.get(id=id)
       return render(request, 'member/update.html', {"mem": member})
    else :  #POST 방식. : 수정
        member = Member.objects.get(id=id) 
        #request.POST['pass'] : 입력된 비밀번호
        #member.pass1 : db에 저장된 비밀번호
        if member.pass1 == request.POST['pass'] : #비밀번호 일치
           member = Member(id=request.POST['id'],
                           name=request.POST['name'],\
                           pass1=request.POST['pass'],
                           gender=request.POST['gender'],\
                           tel=request.POST['tel'],
                           email=request.POST['email'],\
                           picture=request.POST['picture'])
           member.save() #id존재하면, 수정. id값없으면 추가
           #member.delete() : id값에 해당하는 레코드 삭제
           return HttpResponseRedirect("../../info/"+id+"/")
        else :  #비밀번호 오류
           context = {"msg": "회원 정보 수정 실패. \\n비밀번호 오류 입니다.",\
                    "url": "../../update/"+id+"/"}
           return render(request, 'alert.html', context)

def delete(request,id) :
    try :
        login = request.session["login"]
    except :
        context = {"msg": "3.로그인 하세요.", "url": "../../login/"}
        return render(request, 'alert.html', context)
    if login == id :  #관리자도 다른 회원 탈퇴 불가 
        return delete_rtn(request,id)
    else :
        context = {"msg": "3.본인만 탈퇴 가능합니다.", "url": "../../main/"}
        return render(request, 'alert.html', context)
def delete_rtn(request,id) :
    if request.method != 'POST':
       return render(request, 'member/delete.html', {"id":id})
    else :
        member = Member.objects.get(id=id)
        if member.pass1 == request.POST['pass'] : #비밀번호 일치
            member.delete() #db에서 삭제
            auth.logout(request) #세션 종료. 로그아웃 상태
            context = {"msg": "회원님 탈퇴처리가 완료 되었습니다.", \
                       "url": "../../login/"}
            return render(request, 'alert.html', context)
        else : #비밀번호 오류
           context = {"msg": "비밀번호 오류 입니다.", "url": "../../delete/"+id+"/"}
           return render(request, 'alert.html', context)
       
        
'''
  비밀번호 수정 검증 : 
    1. 로그인 필요
    2. 본인 정보만 수정 가능
    
    3. GET : passwordform.html 출력
       POST: password.html 출력
          - 비밀번호 수정 완료 
             opener 창의 url을 /info/id/로 변경.
             현재창은 종료
          - 비밀번호입력 오류
             현재창으로  passwordform.html 출력
'''       

def password(request,id) :
    try :
        login = request.session["login"]
    except :
        context = {"msg": "로그인 하세요.", "url": "../../login/"}
        return render(request, 'alert.html', context)

    if login == id :
        return password_rtn(request,id)
    else :
        context = {"msg": "본인 정보만 수정가능합니다.", "url": "../../main/"}
        return render(request, 'alert.html', context)

def password_rtn(request,id) :
    if request.method != 'POST':
       return render(request, 'member/passwordform.html', {"id":id})
    else :
        member = Member.objects.get(id=id)
        if member.pass1 == request.POST['pass'] :
            member.pass1 = request.POST['chgpass']
            member.save()
            context = {"msg": "비밀번호 수정이 완료 되었습니다.",\
                       "url": "../../info/" + id + "/","closer":True}
            return render(request, 'member/password.html', context)
        else :
           context = {"msg": "비밀번호 오류 입니다.", \
                      "url": "../../password/"+id+"/","closer":False}
           return render(request, 'member/password.html', context)

'''
   회원목록 보기
   1. 관리자만 조회 가능.
   2. 모든 회원정보 조회 : Member.objects.all() => Member 객체의 List로 리턴
   3. 회원정보 목록 list.html 템플릿으로 전달
'''
def list(request) :
    try :
        login = request.session["login"]
    except :
        context = {"msg": "로그인 하세요.", "url": "../login/"}
        return render(request, 'alert.html', context)
        
    if login == 'admin' :  #관리자로 로그인. 정상상태  
       #Member.objects.all() : member테이블의 모든 레코드를 리스트 리턴
        member = Member.objects.all() #회원목록. 리스트
        return render(request, 'member/list.html', {"mlist": member})
    else :  #관리자 아닌 상태
        context = {"msg": "관리자만 조회 가능 합니다.", "url": "../main/"}
        return render(request, 'alert.html', context)
    
    
# BASE_DIR 폴더 하위에  file\picture 폴더 생성 => 파일 업로드 폴더
def picture(request) :
    if request.method != 'POST':
       return render(request, 'member/pictureform.html')
    else :
        # <input type="file" name="picture">
        #fname : 선택한 파일의 이름
        fname = request.FILES['picture'].name #파일이름
        #request.FILES['picture'] : 업로드된 파일 정보
        handle_upload(request.FILES['picture'])
        return render(request, 'member/picture.html', {'fname': fname})

def handle_upload(f):
    #업로드된 파일의 저장 위치 : file/picture/" + f.name
    #wb+ : writer,binary => 이미지 파일은 binary형태로 저장해야 함.
    with open("file/picture/" + f.name, 'wb+') as destination:
        #f.chunks() : 파일의 내용을 읽기.
        for ch in f.chunks():
            destination.write(ch) #파일 쓰기

'''
   게시판 APP 생성하기
   python manage.py startapp board
'''
