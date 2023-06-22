import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd 
from moviepy.editor import *
from tkinter.messagebox import *

root = tk.Tk()
mainvideo = None
mainloc = ''

def select_file():
    return fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])

def select_output():
    return fd.askdirectory(
        title='Open a folder',
        initialdir='/'
    )

def loadvideo():
    global mainvideo
    global mainloc
    mvideo = select_file()
    if mvideo == '': return
    mainloc = mvideo
    mainvideo = VideoFileClip(mvideo)
    updateifo = 'frames : '+str(mainvideo.reader.nframes) + ' (' + str(mainvideo.duration) + 's) '+str(mainvideo.fps)+'fps'
    updateifo += '\n('+str(mainvideo.w)+'x'+str(mainvideo.h)+')'
    l_framecount.config(text=updateifo)
    l_fps.config(text='FPS (max = '+str(mainvideo.fps)+') : ')
    s_fps.config(to=mainvideo.fps)

def gifoutput():
    global mainvideo
    global mainloc
    if mainvideo == None: return
    b_genvideo.config(text='변환 중...')
    finalvideo = mainvideo
    finalvideo = finalvideo.resize(int(v_scale.get())/100)
    finalvideo.write_gif((mainvideo.filename+'.gif'),fps=int(v_fps.get()),program='ffmpeg',logger='bar',fuzz=10)
    b_genvideo.config(text='변환 시작')
    showinfo('done','done')

def predictfile(a,b,c):
    global mainvideo
    if mainvideo == None: return
    finalvideo = mainvideo
    if v_scale.get() == '': return
    finalvideo = finalvideo.resize(int(v_scale.get())/100)
    updateifo = 'frames : '+str(mainvideo.reader.nframes) + ' (' + str(mainvideo.duration) + 's) '+str(mainvideo.fps)+'fps'
    updateifo += '\n('+str(mainvideo.w)+'x'+str(mainvideo.h)+')'
    updateifo += ' to ('+str(finalvideo.w)+'x'+str(finalvideo.h)+') '

# gui ---------------------------------------------------------------
root.title('gif maker')
root.resizable(False,False)
root.geometry('200x200')
b_select_file = ttk.Button(
    root,
    text='파일 선택',
    command=loadvideo
)
b_select_file.pack(expand=True)
b_select_file.place(x=1,y=1,width=190,height=30)
b_genvideo = ttk.Button(
    root,
    text='변환 시작',
    command=gifoutput
)
b_genvideo.pack(expand=True)
b_genvideo.place(x=1,y=150,width=190,height=30)

l_framecount = ttk.Label(
    root,
    text='파일을 선택하세요'
)
l_framecount.pack(expand=True)
l_framecount.place(x=1,y=30,width=190,height=30)

l_fps = ttk.Label(
    root,
    text='FPS (max = 60) : '
)
l_fps.pack(expand=True)
l_fps.place(x=1,y=90,width=105,height=30)

l_scale = ttk.Label(
    root,
    text='Scale (%) : '
)
l_scale.pack(expand=True)
l_scale.place(x=1,y=120,width=105,height=30)

v_fps = tk.StringVar(value=30)
s_fps = ttk.Spinbox(
    root,
    from_=1,
    to=60,
    textvariable=v_fps
)
s_fps.pack(expand=True)
s_fps.place(x=120,y=95,width=60,height=20)

v_scale = tk.StringVar(value=100)
s_scale = ttk.Spinbox(
    root,
    from_=1,
    to=100,
    textvariable=v_scale
)
s_scale.pack(expand=True)
s_scale.place(x=120,y=125,width=60,height=20)
v_scale.trace('w',predictfile)

root.mainloop()
