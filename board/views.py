from django.shortcuts import render

# Create your views here.
# board/views.py

from django.core.paginator import  Paginator
from .models import Board
from django.http import HttpResponseRedirect
from django.utils import timezone

def list(request) :
    #Get 방식의 pageNum 파라미터 조회.  
    #  pageNum 파라미터값이 없는 경우 1로 리턴
    pageNum = int(request.GET.get("pageNum",1)) 
    #Board.objects.all() : Board 데이터 전부 리턴.
    #order_by("-num") : num 컬럼의 내림차순 정렬 
    all_boards = Board.objects.all().order_by("-num")
    #Paginator : all_boards 데이터를 10개씩 나눠서 분리.
    paginator = Paginator(all_boards,10)
    # pageNum 번째 데이터를 리턴 
    # board_list : pageNum에 해당하는 게시물 목록 저장
    board_list = paginator.get_page(pageNum)
    listcount=Board.objects.count() #게시물 등록 건수
    return render(request,'board/list.html',{'board':board_list, 'listcount':listcount})


def write(request) :
    if request.method != 'POST' :  #GET 방식 요청
        return render(request,'board/write.html')
    else :      #POST 방식 요청. 파일업로드, 파라미터값을 db에 저장
        #파일 업로드
        try :
            filename = request.FILES["file1"].name # 업로드 파일의 이름
            #request.FILES["file1"] : file1의 내용
            handle_upload(request.FILES["file1"]) #업로드 파일이름으로 파일 저장
        except:
            filename=""
        #timezone.now() : 현재시간 
        #num 컬럼은 설정하지 않음 : num은 기본키, auto_increments로 설정됨.
        b = Board(name=request.POST["name"],pass1=request.POST["pass"],\
                  subject=request.POST["subject"],content=request.POST['content'],\
                  regdate=timezone.now(),readcnt=0,file1=filename )    
        b.save()   #insert          
        return HttpResponseRedirect("../list")

def handle_upload(f):  #file/board 폴더 생성.
    with open("file/board/"+f.name,"wb+") as dest :
        for ch in f.chunks() :
            dest.write(ch) #파일 저장. 

def info(request, num):
    board = Board.objects.get(num=num)  #num에 해당하는게시물 데이터 조회
    board.readcnt += 1
    board.save()   # 조회수 증가 수정
    return render(request, 'board/info.html', {'b': board})



def update(request, num):
    if request.method != 'POST':
        board = Board.objects.get(num=num) #조회 수 증가 안됨. 
        return render(request, 'board/update.html',{'b': board})
    else :
        '''
        1. 비밀번호 검증
           비밀번호 오류시 : 비밀번호 오류 메시지 출력 후 update 페이지 이동
        2. 내용 수정
           첨부파일의 수정이 없으면, file2 파라미터의 값을 file1에 저장
           수정완료 : 게시판 목록 보기
           수정 실패 : 게시판 수정 실패 메시지 출력 후 update 페이지 이동
        '''
        board = Board.objects.get(num=num) #num에 해당하는 게시물 데이터 조회
        pass1 = request.POST["pass"] # 입력된 비밀번호
        if board.pass1 != pass1 :
            context = {'msg':'비밀번호가 틀립니다.','url':'../../update/'+str(num)+'/'}
            return render(request,'alert.html',context)
        try : 
            handle_upload(request.FILES['file1']) #첨부 파일 수정.
            filename = request.FILES['file1'].name
        except :
            filename = ''
        try :    
            if filename == "" : #첨부파일 수정 안된경우.
                filename = request.POST["file2"]
        
            b = Board(num=request.POST['num'],name=request.POST['name'],\
                      pass1=request.POST['pass'],subject=request.POST['subject'],\
                      content=request.POST['content'],regdate=timezone.now(),\
                      readcnt = 0,file1=filename)
            b.save()
            return HttpResponseRedirect("../../list/")
        except :
            context = {'msg':'게시물 수정 실패','url':'../../update/'+str(num)+'/'}
            return render(request,'alert.html',context)

'''
    GET : 해당 화면 출력
    POST : 
        1. 비밀번호 검증
            오류 : '비밀번호 오류' 메세지 출력. delete 페이지 출력
        2. 해당 게시물 삭제.
            게시물 목록 출력
'''        
def delete(request,num) :
    if request.method != 'POST':
        return render(request, 'board/delete.html', {"num":num})
    else :
        board = Board.objects.get(num=num)
        pass1 = request.POST["pass"]
        if board.pass1 == pass1 :
            board.delete()
            return HttpResponseRedirect("../../list/")
        
        else : # 비밀번호 오류
            context = {'msg':'비밀번호가 틀립니다.','url':'../../delete/'+str(num)+'/'}
            return render(request, 'alert.html', context)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        