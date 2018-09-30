from tkinter import *
import tkinter.ttk as ttk
from fractions import Fraction
import simplexlib

'''
label_mtrx = []
entry_mtrx = []
sign_mtrx = []
result_mtrx = []
target = 0

def click_solve_btn():
    #Проверка введённых даных на корректность
    simplexlib.

root = Tk()
root.title("Графическая программа на Python")
#root.geometry("600x600")

n = IntVar()
n.trace("w", lambda name, index, mode, n=n: placetable(n))
n.set(3)
m = IntVar()
m.set(3)

labelintro = Label(text="Решение задачи линейного программирования симплекc-методом", height=2)
labelintro.pack(side=TOP)

frame1 = Frame(root, bg='green')
frame1.pack(side=TOP)

framemtrx = Frame(root)
framemtrx.pack(side=TOP)

solve_btn = Button(text="Решить", command=click_solve_btn)
solve_btn.pack(side=TOP)

labeln = Label(frame1, text="Количество строк")
labeln.pack(side=LEFT)

entryn = Spinbox(frame1, from_=1, to=7, textvariable=n)
entryn.pack(side=LEFT)
labelm = Label(frame1, text="Количество столбцов")
labelm.pack(side=LEFT)
entrym = Spinbox(frame1, from_=1, to=7, textvariable=m)
entrym.pack(side=LEFT, fill=X)


for i in range(n.get()+1):
    label_mtrx.append([])
    entry_mtrx.append([])
    for j in range(m.get()):
        if j==m.get()-1:
            eq = ''
        else:
            eq = '+'
        entry_mtrx[i].append(Entry(framemtrx, width=5, justify=RIGHT))
        entry_mtrx[i][j].grid(row=i, column=2*j, pady=1)
        label_mtrx[i].append(Label(framemtrx, text="x{} {}".format(j, eq)))
        label_mtrx[i][j].grid(row=i, column=2*j+1, pady=1)
    if i==n.get():
        Label(framemtrx, text="→").grid(row=i, column=2*m.get()+2, pady=1)
        target = ttk.Combobox(framemtrx, width=4)
        target['values'] = ['min', 'max']
        target.current(0)
        target.grid(row=i, column=2*m.get()+3, padx=5, pady=1)
    else:
        sign_mtrx.append(ttk.Combobox(framemtrx, width=1))
        sign_mtrx[i]['values'] = ['≤', '≥', '=']
        sign_mtrx[i].current(0)
        sign_mtrx[i].grid(row=i, column=2*m.get()+2, pady=1)
        result_mtrx.append(Entry(framemtrx, width=7))
        result_mtrx[i].grid(row=i, column=2*m.get()+3, padx=5, pady=1)

root.mainloop()
'''
class Application(Frame):
    def __init__(self, parent):
        self.N = 3
        self.M = 3
        self.label_mtrx = []
        self.entry_mtrx = []
        self.sign_mtrx = []
        self.result_mtrx = []
        self.target = 0
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.create_widgets()
    
    #Функция печати на экран пошагового решения
    def print_solution(self, solution):
        Label(self, text="Этап 1. Поиск опорного решения:").pack()
        for table in solution['mtrx1']:
            frame = Frame(self)
            frame.pack()
            for i in range(len(table)):
                for j in range(len(table[1])):
                    if i==0:
                        if j==0:
                            Label(frame, text=" ").grid(row=i, column=j, padx=1, pady=1)
                        else:
                            Label(frame, text=str(table[i][j-1])).grid(row=i, column=j, padx=1, pady=1)
                    else:
                        Label(frame, text=str(table[i][j])).grid(row=i, column=j, padx=1, pady=1)
        if solution['error1']!='None':
            Label(self, text=solution['error1']).pack()
            return
        Label(self, text="В столбце свободных членов нет отрицательных - опорное решение найдено.").pack()
        Label(self, text="Этап 2. Поиск оптимального решения:").pack()
        for table in solution['mtrx2']:
            frame = Frame(self)
            frame.pack()
            for i in range(len(table)):
                for j in range(len(table[1])):
                    if i==0:
                        if j==0:
                            Label(frame, text=" ").grid(row=i, column=j, padx=1, pady=1)
                        else:
                            Label(frame, text=str(table[i][j-1])).grid(row=i, column=j, padx=1, pady=1)
                    else:
                        Label(frame, text=str(table[i][j])).grid(row=i, column=j, padx=1, pady=1)
        if solution['error2']!='None':
            Label(self, text=solution['error2']).pack()
            return
        Label(self, text="В строке коэффициентов целевой функции нет положительных элементов - оптимальное решение найдено.").pack()
        #Печать ответа
        Label(self, text="Ответ:").pack()
        framesolve = Frame(self)
        framesolve.pack()
        sln = dict([[row[0], str(row[1])] for row in solution['mtrx2'][-1] if row[0]!='s0'])
        sol = {}
        for i in range(1, self.M+1):
            sol['x{}'.format(i)] = sln.get('x{}'.format(i), '0')
        sol['F'] = sln['F'] if self.target.get()=='min' else str(-Fraction(sln['F']))
        for i in range(len(list(sol.items()))):
            Label(framesolve, text=list(sol.items())[i][0]).grid(row=0, column=i, padx=1, pady=1)
            Label(framesolve, text=list(sol.items())[i][1]).grid(row=1, column=i, padx=1, pady=1)

    #Функция обработки нажатия на кнопку "Решить"
    def click_solve_btn(self):
        mtrx = []
        for i in range(len(self.entry_mtrx)):
            mtrx.append([])
            for j in range(len(self.entry_mtrx[0])+1):
                try:
                    if j!=0:
                        additem = Fraction(self.entry_mtrx[i][j-1].get())
                    else:
                        if i!=self.N:
                            additem = Fraction(self.result_mtrx[i].get())
                        else:
                            additem = Fraction(0)
                except Exception:
                    self.entry_mtrx[i][j-1]['bg'] = 'red'
                    return
                self.entry_mtrx[i][j-1]['bg'] = 'white'
                if i==self.N:
                    if self.target.get()=='max':
                        mtrx[i].append(additem)
                    else:
                        mtrx[i].append(-additem)
                else:
                    if self.sign_mtrx[i].get()=='≥':
                        mtrx[i].append(-additem)
                    else:
                        mtrx[i].append(additem)
        varlist = []
        varlist.append(['s0'])
        for i in range(self.M):
            varlist[0].append("x{}".format(i+1))
        varlist.append(["x{}".format(i) for i in range(self.M+1, self.M+self.N+1)])
        varlist[1].append("F")

        res = simplexlib.solve_simplex(mtrx, varlist)
        self.print_solution(res)

    #Функция размещения виджетов на экране
    def create_widgets(self):
        self.labelintro = Label(self, text="Решение задачи линейного программирования симплекc-методом", height=2)
        self.labelintro.pack(side=TOP)
        '''
        self.frame1 = Frame(self, bg='green')
        self.frame1.pack(side=TOP)
        '''
        self.framemtrx = Frame(self)
        self.framemtrx.pack(side=TOP)

        self.solve_btn = Button(self, text="Решить", command=self.click_solve_btn)
        self.solve_btn.pack(side=TOP)
        '''
        self.labeln = Label(frame1, text="Количество строк")
        self.labeln.pack(side=LEFT)

        self.entryn = Spinbox(frame1, from_=1, to=7, textvariable=n)
        self.entryn.pack(side=LEFT)

        self.labelm = Label(frame1, text="Количество столбцов")
        self.labelm.pack(side=LEFT)

        self.entrym = Spinbox(frame1, from_=1, to=7, textvariable=m)
        self.entrym.pack(side=LEFT, fill=X)
        '''
        for i in range(self.N+1):
            self.label_mtrx.append([])
            self.entry_mtrx.append([])
            for j in range(self.M):
                if j==self.M-1:
                    eq = ''
                else:
                    eq = '+'
                self.entry_mtrx[i].append(Entry(self.framemtrx, width=5, justify=RIGHT))
                self.entry_mtrx[i][j].grid(row=i, column=2*j, pady=1)
                self.label_mtrx[i].append(Label(self.framemtrx, text="x{} {}".format(j+1, eq)))
                self.label_mtrx[i][j].grid(row=i, column=2*j+1, pady=1)
            if i==self.N:
                Label(self.framemtrx, text="→").grid(row=i, column=2*self.M+2, pady=1)
                self.target = ttk.Combobox(self.framemtrx, width=4)
                self.target['values'] = ['min', 'max']
                self.target.current(0)
                self.target.grid(row=i, column=2*self.M+3, padx=5, pady=1)
            else:
                self.sign_mtrx.append(ttk.Combobox(self.framemtrx, width=1))
                self.sign_mtrx[i]['values'] = ['≤', '≥', '=']
                self.sign_mtrx[i].current(0)
                self.sign_mtrx[i].grid(row=i, column=2*self.M+2, pady=1)
                self.result_mtrx.append(Entry(self.framemtrx, width=7))
                self.result_mtrx[i].grid(row=i, column=2*self.M+3, padx=5, pady=1)

if __name__=="__main__":
    root = Tk()
    root.title = "Симплекс-метод"
    app = Application(root)
    app.mainloop()
