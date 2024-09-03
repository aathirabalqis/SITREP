import os
import pandas as pd 
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

root = Tk()

root.title('AMI - SITREP')
root.geometry('300x150')
# root.config(bg = 'thistle1')

# nb = ttk.Notebook(root)

# bcrm = ttk.Frame(nb)
# mdms = ttk.Frame(nb)

# nb.add(bcrm, text = 'BCRM')
# nb.add(mdms, text = 'MDMS')
# nb.place(x = 30, y = 30)

def getbcrm():
    global bcrm
    bcrm = fd.askopenfilenames(filetypes=[("Text files","*.txt")])
    Label(root, text = bcrm).place(x = 165, y  = 42)
    
    return bcrm

def clean():
    
    folder = '\\'.join(bcrm[0].split('/')[:-1])
    first = ''
    flag = 0
    bigdf = pd.DataFrame()
    
    for i in bcrm:
        filename = i.split('/')[-1].split('.')[0]
        t = open(folder + '\\' + 'temp.txt','w', encoding = 'utf-8')
        
        with open(i, 'r') as f:
            for line in f.readlines():
                # print('in')
                if '|' in line:
                    if len(line.replace('|','').replace('-','')) > 5:
                        t.write(line.replace('|"','|'))
                    
        f.close()
        t.close()
        print('done')
        
        # dtypes = {'Telephone No.': 'string', 'Installation Type': 'string', 'Voltage Level':'string'}

        df = pd.read_csv(folder + '\\temp.txt', sep = '|', dtype = str)
        # df = df.drop_duplicates()
        
        
        
        # delete rows that mimic header
        # df = df.drop(df.index[df['State'] == 'State'].tolist())
        df = df.drop(df.index[df['State'] == 'State'].tolist())
        df = df[df.columns[1:-1]]
        df = df.rename(columns = lambda x: x.strip())
        
        # df['Installation Type'] = df['Installation Type'].apply(lambda x: str(x) + ' ')
        # df['Telephone No.'] = df['Telephone No.'].apply(lambda x: ' ' + str(x) + ' ')
        
        # print(df['Installation Type'])
        
        # # df['Telephone No.'] = df['Telephone No.'].apply('"{}"'.format)
        # # df['Installation Type'] = df['Installation Type'].apply('"{}"'.format)
        # df['Voltage Level'] = df['Voltage Level'].apply('"{}"'.format)
        # df['Voltage Level'] = df['Voltage Level'].str.replace('"','')
        
        
        
        # df = df.astype(str)
        
        # print(df['Telephone No.'])
        
        # # df['Telephone No.'] = df['Telephone No.'].astype(str).apply(lambda x : '0' + x if df['Telephone No.'].str.len() >= 8 else x)
        # df.loc[(df['Telephone No.'].str.len() >= 8) & (pd.isnull(df['Telephone No.']) == False), 'Telephone No.'] = '0' + df['Telephone No.']
        # df.loc[(df['Rate Category'].str.len() == 1), 'Rate Category'] = '0' + df['Rate Category']
        # df.loc[(df['Voltage Level'].str.len() == 1), 'Voltage Level'] = '0' + df['Voltage Level']
        
        # print(df['Telephone No.'])
        df.to_csv(folder + '\\' + filename + '.csv', index = False)
        print('done pt 2')
        bigdf = pd.concat([bigdf, df])
    
    
    bigdf.to_csv(folder + '\\' + '_'.join(filename.split('_')[:-1]) + '.csv', index = False)
    os.remove(folder + '\\' + 'temp.txt')
        

def test():
    print('h')
def exitt(event):
    root.quit()

Button(root, text = 'Upload BCRM', command = getbcrm).place(x = 38, y = 40) 
Label(root, text = 'Path:').place(x = 130, y  = 42) 

Button(root, text = 'Clean Files', command = clean).place(x = 101, y = 90)
# Button(root, text = 'Format Files', command = test).place(x = 101, y = 110)

root.bind('<Escape>', exitt)
root.mainloop()