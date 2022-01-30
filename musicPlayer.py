from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from pygame import *
import os
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from mutagen.mp3 import MP3
import math
import time

top = Tk()
top.title('Music Player')
top.geometry('320x480')

canvas = Canvas(top, width = 320, height = 480)
canvas.pack(expand=True, fill='both')

mixer.init()                            # pygame.mixer : 사운드 로드, 재생
mixer.music.set_volume(0.5)

# variable
list_music = []
list_music_path = []
index = 0
lb_string = StringVar()                     # label, Text의 값 즉시 바뀜 (변수 = '문자열' X)
vol_size = DoubleVar()
volumn = 0.5                                # 0.0 ~ 1.0

#fuction
def music_list(event):                           # b_list 함수: 재생목록
    global index
    
    def insert_musics(event):
        dir = askdirectory()
        #os.chdir(dir)                           # chdir (현재경로 바꾸기)
        
        #if not os.path.exists('./myplayList'):
        input_music(dir)
    
    def insert_music(event):
        # add one file
        # dir = filedialog.askopenfilename(initialdir='/', title='select file', filetypes=(('mp3 Files', '*.mp3'),))
        # input_music(dir)
        
        # add many file
        files = filedialog.askopenfilenames(initialdir='/', title='select file', filetypes=(('mp3 Files', '*.mp3'),))
        
        for file in files:
            input_music(file)

    def input_music(dir):
        if os.path.isfile(dir):
            file_arr = dir.split('.')
            if file_arr[-1] == 'mp3' or file_arr[-1] == 'wav' or file_arr[-1] == 'ogg':
                fName = dir.split('/')
                list_music.append(fName[-1])
                list_music_path.append(dir)
                lb.insert(END, fName[-1])
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                file_arr = file.split('.')
                #print(file_arr[1])
                if file_arr[-1] == 'mp3' or file_arr[-1] == 'wav' or file_arr[-1] == 'ogg':
                    fName = file.split('/')
                    list_music.append(fName[-1])
                    lb.insert(END, fName[-1])
                    
                    file_full_path = os.path.join(dir, file)
                    list_music_path.append(file_full_path)
                    print(file_full_path)
                
                
        
        #mixer.init()                            # pygame.mixer : 사운드 로드, 재생
        #mixer.music.load(list_music[index])    # list_music[0] 파일 로드 / wav, mp3, ogg
        #mixer.music.play()                     # 재생
        #mixer.music.set_volume(0.5)
        #list_win.update()
    
    def path_check(file_path):
        assemble_path= ''
        cur_path = os.getcwd()
        print('현재 폴더 경로:',cur_path)
        print('선택 파일 경로:', file_path)
        file_path_arr = file_path.split('\\') #print(file_path_arr)
        
        for x in range(len(file_path_arr)-1):
            assemble_path += file_path_arr[x] +'\\'
        #print('조립된 경로:',assemble_path)# print(assemble_path[:-1])
        
        if cur_path != assemble_path[:-1]:
            mixer.music.pause()
            os.chdir(assemble_path[:-1])
        ch_cur_path = os.getcwd()
        print('ch: ',ch_cur_path)
        list_win.update() #list_win.update_idletasks()

    def list_select(event):
        global index
        global song_length
        
        lb_string.set('')
        index = int(lb.curselection()[0])           # 커서로 선택 #lb.curselection()[0] 
        print(index) 
        
        song_mut = MP3(list_music_path[index])      # mp3 파일 길이---- play_time()으로 이동
        song_length = song_mut.info.length
        print(song_length)                          # 나중에 레이블로 표시해주기
        
        mixer.music.load(list_music_path[index])
        
        mixer.music.play(-1)
        lb_string.set(list_music[index])            # 이름 레이블에 세팅
        hide_play()
        canvas.itemconfig(can_cover, state='normal')
        volumn_lb.place(x=20, y=150)
        
        # slider update
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=0) # 시작 시 값 0 # pygame.mixer.music. set_pos ( ) 재생할 위치  / pygame.mixer.music. get_pos ( ) 
        

    def list_insert():
        i = 0
        for music in list_music:
            lb.insert(i, music)
            i+=1
            
    list_win = Toplevel(top)                    # list_win 창 맨위에
    list_win.title('파일목록')
    scroll = Scrollbar(list_win)
    scroll.pack(side=RIGHT, fill=Y)
    
    insert_label = Label(list_win, text='폴더로 가져오기')
    # insert_label.pack(fill=NONE, padx=0, pady=0)
    insert_label.place(x=0, y=2)
    insert_label.bind('<Button-1>', insert_musics)
    insert_label2 = Label(list_win, text='파일 가져오기')
    # insert_label2.pack(fill=NONE, padx=30)
    insert_label2.place(x=100, y=2)
    insert_label2.bind('<Button-1>', insert_music)
    
    lb = Listbox(list_win, width=50, yscrollcommand=scroll.set)
    lb.pack(side=LEFT, pady=25)
    
    scroll.config(command = lb.yview)           # (config: 수정) 삭제 추가 시 Listbox 조절
    music_lb = Label(canvas, textvariable=lb_string)
    music_lb.pack(side='bottom', pady=165)
    list_insert()

    lb.bind("<<ListboxSelect>>", list_select)   # listbox 선택 시 이벤트

def music_play(event): # takes 0 positional arguments but 1 was given
    #mixer.music.play() # play(-1) : 무한 반복
    mixer.music.unpause()
    canvas.itemconfig(can_play, state='hidden')
    canvas.itemconfig(can_stop, state='normal')

def music_stop(event):
    #mixer.music.stop()
    mixer.music.pause()
    canvas.itemconfig(can_stop, state='hidden')
    canvas.itemconfig(can_play, state='normal')

def music_next(event):
    global index
    index += 1
    
    if index >= len(list_music):
        index = 0
    print(index)
    mixer.music.load(list_music_path[index])
    mixer.music.play(-1)                 # 무한 반복
    lb_string.set(list_music[index])
    
    # slider update
    slider_position = int(song_length)
    my_slider.config(to=slider_position, value=0)

def music_back(event):
    global index
    global song_length
    index -= 1
    if index < 0:
        index = len(list_music) - 1

    mixer.music.load(list_music_path[index])
    mixer.music.play(-1)                 # 무한 반복
    lb_string.set(list_music[index])
    
    # slider update --> 현재 재생중인 노래 길이 알아야함.. 위에 select햇을 때만 업뎃되면X
    slider_position = int(song_length)
    my_slider.config(to=slider_position, value=0)

def volumn_up(event):
    global volumn
    volumn += 0.1
    if volumn > 1.0:
        volumn = 1.0
    mixer.music.set_volume(volumn)
    vol = round(volumn,2)*10
    vol_size.set(math.ceil(vol))
    print(vol)

def volumn_down(event):
    global volumn
    volumn -= 0.1
    if volumn < 0.0:
        volumn = 0.0
    mixer.music.set_volume(volumn)
    vol = round(volumn,2)*10
    print(vol)
    vol_size.set(math.ceil(vol))

def quit_music():
        mixer.music.stop()
        top.destroy()

# def hide_play():
#     b_play.place_forget()           # b_stop.pack_forget()
#     b_stop.place(x=167, y=380)
# def hide_stop():
#     b_stop.place_forget()           # b_stop.pack_forget()
#     b_play.place(x=122, y=380)
    
def hide_play():
    canvas.itemconfig(can_play, state='hidden')
    canvas.itemconfig(can_stop, state='normal')
    
def hide_stop(event):
    canvas.itemconfig(can_stop, state='hidden')
    canvas.itemconfig(can_play, state='normal')

# time (여기에 음악 길이 포함시키기)
def play_time():
    current_time = mixer.music.get_pos() / 1000     # 재생시간 가져오기
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    
    # mp3파일 길이
    global song_length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    
    ##
    my_slider.config(value=current_time)
    

def slide(x):
    slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
#slider
def slider(x):
    mixer.music.load(list_music_path[index])
    mixer.music.play(-1, start=int(my_slider.get()))


#ui
# 배경
bgImage = ImageTk.PhotoImage(Image.open("button/water.png")) 
bg = canvas.create_image(0, 0, image=bgImage, anchor=NW)

img_play = ImageTk.PhotoImage(Image.open('button/play.png'))
can_play = canvas.create_image([142,380], anchor=NW,  image=img_play)
canvas.image_names=img_play

img_stop = ImageTk.PhotoImage(Image.open('button/pause.png'))
can_stop = canvas.create_image([142,380], anchor=NW,  image=img_stop, state='hidden')
canvas.image_names=img_stop

img_back = ImageTk.PhotoImage(Image.open('button/back.png'))
can_back = canvas.create_image([60,380], anchor=NW,  image=img_back)
canvas.image_names=img_back

img_next = ImageTk.PhotoImage(Image.open('button/next.png'))
can_next = canvas.create_image([220,380], anchor=NW,  image=img_next)
canvas.image_names=img_next

img_up = ImageTk.PhotoImage(Image.open('button/up.png'))
can_up = canvas.create_image([142,330], anchor=NW,  image=img_up)
canvas.image_names=img_up

img_down = ImageTk.PhotoImage(Image.open('button/down.png'))
can_down = canvas.create_image([142,430], anchor=NW,  image=img_down)
canvas.image_names=img_down

img_list = ImageTk.PhotoImage(Image.open('button/list.png'))
can_list = canvas.create_image([30,330], anchor=NW,  image=img_list)
canvas.image_names=img_list

# volumn label
vol_size.set(math.ceil(round(volumn,2)*10))
volumn_lb = Label(top, textvariable=vol_size) # mixer.music.get_volume  /  textvariable=vol_string
# volumn_lb.place(x=20, y=150)                  # 처음에 가렷다가 버튼누르면 띄워주자
volumn_lb.place_forget()

#canvas.create_rectangle(50, 30, 270, 250, fill='#C2CFBD', outline='white') # x1y1 , x2y2 '#c6d57e' d3d3d3
img_cover = ImageTk.PhotoImage(Image.open('button/cover.png'))
can_cover = canvas.create_image([50,30], anchor=NW,  image=img_cover, state='hidden')
canvas.image_names=img_cover

# slider
my_slider = ttk.Scale(top, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=280)
my_slider.pack()#
# 임시 슬라이더
slider_label = Label(top, text='0')
slider_label.place(x=10, y=10)


# 이벤트
# b_play.bind('<Button-1>', music_play)
# b_stop.bind('<Button-1>', music_stop)
# b_next.bind('<Button-1>', music_next)
# b_back.bind('<Button-1>', music_back)
# b_up.bind('<Button-1>', volumn_up)
# b_down.bind('<Button-1>', volumn_down)
canvas.tag_bind(can_play, "<Button-1>", music_play)
canvas.tag_bind(can_stop, "<Button-1>", music_stop)
canvas.tag_bind(can_back, "<Button-1>", music_back)
canvas.tag_bind(can_next, "<Button-1>", music_next)
canvas.tag_bind(can_up, "<Button-1>", volumn_up)
canvas.tag_bind(can_down, "<Button-1>", volumn_down)
canvas.tag_bind(can_list, "<Button-1>", music_list)


top.protocol('WM_DELETE_WINDOW', quit_music)
top.mainloop()






# < 기능 >
#----> 완료 # 1. [ui] play누르면 stop 버튼 가리기  
# 1-1. 창 크기 고정시키기
# 2. [music_list()] list_win 안에 폴더추가 버튼 생성 + 들어가자마자 저 창 뜨지않게
#----> 완료 # 3. [music_list()] 파일목록에 파일 데려올 때 mp3, wma등 노래 파일만 zip파일X
# 4. 재생 스크롤 만들기
#----> 완료 # 5. 다른 디렉토리에서 불러와도 모두 재상 가능하게 하기
    # 현재 디렉토리에서 파일 불러오면 그 디렉토리에 있는 파일만 재생가능
    # chdir (현재경로 바꾸기) 이거 때문인듯
    # 1) '재생목록' 폴더 생성하고 거기에 파일 복사하기...? (별로인듯 다른 방법 찾기)
    # 2) 파일의 절대경로 찾아서 load시킬때 '절대경로\'+file 로 로드하자
    # 해결 방법: 파일의 절대경로를 담아두는 리스트 생성하여 파일을 list_music에 담을 때 list_music_path에 같이 담앗음
# 6. 재생목록에서 선택한 파일 삭제
    # 만약 '재생목록'파일 있다면, 삭제하면 '재생목록'파일에서도 삭제... (비교해서 같은 파일 잇으면 복사X)
#----> 완료 # 7. 볼륨크기 조절하면 좌측에 레이블 띄우기(생성..)
# 8. 7번의 레이블 2초 띄우고 가리기(삭제)
#----> 완료 # 9. 볼륨크기 레이블 0.0~1.0 -> 정수로 바꿔 표시해주기
# 10. 음악 길이 슬라이더 밑에 표시해주기 (selected() 에 구해둠)

# < 디자인 >
# 1. 배경 이미지 축소 or 작은 이미지
# 2. 버튼 이미지 하얀 글자로 만들기 (확장자 .gif)


# //tkinter// bind Event 종류
# label.bind('<Event>', 함수) : 레이블이나 버튼 등에 이벤트가 일어나면 함수 수행
# 참고: https://lcs1245.tistory.com/entry/Python-tkinter-Bind-Event-%EC%97%B0%EA%B2%B0
# ==Button==
# <Button-1> : 마우스 왼쪽 버튼
# <Button-2> : 마우스 휠 버튼
# <Button-3> : 마우스 오른쪽 버튼
# <Button-4> : 스크롤 업
# <Button-5> : 스크롤 다운
# <MouseWheel> : 마우스 휠 이동
# Motion, Release, DoubleClick, WidgetOperation, KeyInput, Assistant KeyInput

#scrollbar
# command=함수: 스크롤이 active 상태일 때 실행하는 메서드(함수)

# Listbox
# yview() : 세로스크롤

# < 경로명 분리하기 >
# https://eehoeskrap.tistory.com/496
# os.path.splitext(filename) - 확장자와 나머지 분리