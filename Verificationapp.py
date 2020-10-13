from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from reportgen import *
import tkinter as tk
import pandas as pd
import os
import glob
from itertools import groupby, count

guiBackgroundColor = "gray35"
columnsTitle = ['Retract Command', 'Extend Command', 'AG Downlock', 'AG Uplock', 'AGD Open', 'AGD Uplock', 'LG Uplock',
                'LG Downlock', 'RG Uplock', 'RG Downlock', 'Close AG Doors', 'MG Not Downlock', 'Fail ChA', 'Fail ChB',
                'Gear Up Solenoid #2', 'Gear Down Solenoid #2', 'Gear Up Solenoid #3', 'Gear Down Solenoid #3',
                'Door Open Solenoid', 'Door Close Solenoid', 'SBCV Solenoid', 'State']
states_delay = ["Delay Between State (ms)"]

def intervals(data):
    out = []
    counter = count()

    for key, group in groupby(data, key=lambda x: x - next(counter)):
        block = list(group)
        out.append([block[0], block[-1]])
    return out


# First and Main Window of the application
class Verificationapp():

    def __init__(self, master, title, size):
        self.master = master
        self.title = title
        self.master.title(self.title)
        self.size = size
        self.master.geometry(self.size)
        self.master.configure(bg=guiBackgroundColor)
        Button(self.master, text='Single File Test', command=self.singleTestWindow, bg='gainsboro', fg='gray1',
               font=('helvetica', 12, 'bold')).place(relx=0.5, y=100, anchor="center")

        Button(self.master, text='Multiple File Test', command=self.multipleTestWindow, bg='gainsboro', fg='gray1',
               font=('helvetica', 12, 'bold')).place(relx=0.5, y=175, anchor="center")

        Label(self.master, text='Verification Software', bg=guiBackgroundColor, fg='snow',
              font=('helvetica', 15, 'bold')).place(relx=0.5, y=30, anchor="center")
        self.time_tolerance = Entry(self.master, bd=3, width=10)
        Label(self.master, text='Time Tolerance:  ±', bg=guiBackgroundColor, fg='snow',
                                     font=('helvetica', 12, 'bold')).place(relx=0.3, y=240, anchor="center")
        Label(self.master, text='(ms)', bg=guiBackgroundColor, fg='snow',
              font=('helvetica', 12, 'bold')).place(relx=0.84, y=240, anchor="center")
        self.time_tolerance.place(relx=0.66, y=240, anchor="center")

    def singleTestWindow(self):
        try:
            tolerance = int(self.time_tolerance.get())
            obj = VerificationSingleWindow(self, "Run Single Test", "300x300", tolerance)
        except ValueError:
            if not (self.time_tolerance.get()):
                messagebox.showinfo("Error", "Time Tolerance needs an integer value!")
            else:
                messagebox.showinfo("Error", "Time Tolerance only accept integer values!")

    def multipleTestWindow(self):
        try:
            tolerance = int(self.time_tolerance.get())
            obj = VerificationMultipleWindow(self, "Run Multiple Test", "300x330", tolerance)
        except ValueError:
            if not (self.time_tolerance.get()):
                messagebox.showinfo("Error", "Time Tolerance needs an integer value!")
            else:
                messagebox.showinfo("Error", "Time Tolerance only accept integer values!")


# Second window for the Single Test application
class VerificationSingleWindow(Toplevel):

    def __init__(self, parent, title, size, tolerance):
        global toleranceValue
        super().__init__(name='verification_main_menu')
        self.parent = parent
        self.title(title)
        self.geometry(size)
        self.configure(bg=guiBackgroundColor)
        Button(self, text='Import the Testbench .csv file', bg='khaki1', fg='navy', command=self.singleTestbench,
               font=('helvetica', 12, 'bold')).place(relx=0.5, y=100, anchor="center")
        Button(self, text='Import the LabView .csv file', bg='khaki1', fg='navy', command=self.singleLabView,
               font=('helvetica', 12, 'bold')).place(relx=0.5, y=175, anchor="center")
        Button(self, text='Verify Files', command=self.single_verify, bg='gainsboro', fg='gray1',
               font=('helvetica', 10, 'bold')).place(relx=0.5, y=250, anchor="center")
        Label(self, text='Single Test Verification', bg=guiBackgroundColor, fg='snow',
              font=('helvetica', 15,'bold')).pack(fill=X, pady=10)
        self.toleranceValue = tolerance

    def singleTestbench(self):
        global datatb
        global delaytb
        try:
            import_file_path = filedialog.askopenfilename()
            self.input_outputtb = pd.read_csv(import_file_path, dtype="int64")
            self.datatb = self.input_outputtb.reindex(columns=columnsTitle)
            self.delaytb = self.input_outputtb[states_delay]
            messagebox.showinfo("Uploaded File", "File Uploaded!")
        except UnicodeDecodeError:
            messagebox.showinfo("Error", "This is not a .csv file")
        except FileNotFoundError:
            messagebox.showinfo("Error", "Upload file canceled.")

    def singleLabView(self):
        global datalv
        global delaylv
        global filename
        try:
            import_file_path = filedialog.askopenfilename()
            self.input_outputlv = pd.read_csv(import_file_path, dtype="int64")
            self.datalv = self.input_outputlv.reindex(columns=columnsTitle)
            self.delaylv = self.input_outputlv[states_delay]
            filename = os.path.splitext(os.path.basename(import_file_path))[0]
            messagebox.showinfo("Uploaded File", "File Uploaded!")
        except UnicodeDecodeError:
            messagebox.showinfo("Error", "This is not a .csv file")
        except FileNotFoundError:
            messagebox.showinfo("Error", "Upload file canceled.")

    def single_verify(self):
        identicalrow = 0
        differentrow = 0
        wrongioline = []
        wrongdelayline = []
        try:
            report = open(filename + '.html', "w")
            lengrange = min(len(self.datatb), len(self.datalv))
            for rows in range(lengrange):
                dataTBrow = self.datatb.loc[rows, :]
                dataLVrow = self.datalv.loc[rows, :]
                delayTBrow = self.delaytb.values[rows][0]
                delayLVrow = self.delaylv.values[rows][0]

                if dataLVrow.equals(dataTBrow) and (delayLVrow in range((delayTBrow - self.toleranceValue),
                                                                        delayTBrow + self.toleranceValue+1)):
                    identicalrow += 1
                else:
                    if not (delayLVrow in range(delayTBrow - self.toleranceValue,
                                                delayTBrow + self.toleranceValue + 1)):
                        wrongdelayline.append(rows + 2)
                    if not dataLVrow.equals(dataTBrow):
                        wrongioline.append(rows + 2)
                    differentrow += 1
            successmsg = 'Identical rows: ' + repr(identicalrow) + '\nDifferent rows: ' + repr(differentrow)
            messagebox.showinfo("Results", successmsg)
            if differentrow > 0:
                status = "<b>NOT APPROVED</b>"
            else:
                status = "<b>APPROVED</b>"
            resultmsg = reportfile((self.datatb.__len__()), (self.datalv.__len__()), int(identicalrow),
                                   int(differentrow),
                                   wrongioline[:], wrongdelayline[:], filename, status)
            report.write(resultmsg)
            self.destroy()
        except NameError:
            messagebox.showinfo("Results", "Import the files first!")
        except ValueError:
            messagebox.showinfo("Results", "Number of lines does not match! Check file first!")


# Third window for the Multiple Test application
class VerificationMultipleWindow(Toplevel):

    def __init__(self, parent, title, size, tolerance):
        global load_progress
        global toleranceValue
        super().__init__(name='verification_main_menu')
        self.parent = parent
        self.title(title)
        self.geometry(size)
        self.configure(bg=guiBackgroundColor)
        Button(self, text='Import the Testbench .csv file', bg='khaki1', fg='navy', command=self.multipleTestbench,
               font=('helvetica', 12, 'bold')).place(relx=0.5, y=100, anchor="center")
        Button(self, text='Import the LabView folder', bg='khaki1', fg='navy', command=self.multipleLabView,
               font=('helvetica', 12, 'bold')).place(relx=0.5, y=175, anchor="center")
        Button(self, text='Verify Files', command=self.multiple_verify, bg='gainsboro', fg='gray1',
               font=('helvetica', 10, 'bold')).place(relx=0.5, y=250, anchor="center")
        Label(self, text='Multiple Test Verification', bg=guiBackgroundColor, fg='snow',
              font=('helvetica', 15, 'bold')).place(relx=0.5, y=30, anchor="center")
        self.load_progress = Progressbar(self, orient="horizontal", length=100, mode='determinate')
        self.load_progress.place(relx=0.5, y=290, anchor="center")
        self.toleranceValue = tolerance

    def multipleTestbench(self):
        global datatb
        global delaytb
        try:
            import_file_path = filedialog.askopenfilename()
            self.input_outputtb = pd.read_csv(import_file_path, dtype="int64")
            self.datatb = self.input_outputtb.reindex(columns=columnsTitle)
            self.delaytb = self.input_outputtb[states_delay]
            messagebox.showinfo("Uploaded File", "File Uploaded!")
        except UnicodeDecodeError:
            messagebox.showinfo("Error", "This is not a .csv file")
        except FileNotFoundError:
            messagebox.showinfo("Error", "Upload file canceled.")

    def multipleLabView(self):
        global datalv, delaylv
        global filename
        global numFilesLoaded
        global nameframes, dataframes, delayframes
        dataframes = []
        nameframes = []
        delayframes = []
        numFilesLoaded = 0
        try:
            import_folder_path = filedialog.askdirectory()
            csvfiles = glob.glob(os.path.join(import_folder_path, '*.csv'))
            for files in csvfiles:
                filename = os.path.splitext(os.path.basename(files))[0]
                nameframes.append(filename)
                self.df = pd.read_csv(files, dtype="int64")
                dataframes.append(self.df.reindex(columns=columnsTitle))
                self.delaylv = self.df[states_delay]
                delayframes.append(self.delaylv)
                numFilesLoaded += 1
            messagebox.showinfo("Uploaded Folder", "Folder Uploaded!")
        except UnicodeDecodeError:
            messagebox.showinfo("Error", "This is not a folder")
        except FileNotFoundError:
            messagebox.showinfo("Error", "Upload file canceled.")

    def multiple_verify(self):
        differentfiles = 0
        resultmsg = ""
        wrongioline = []
        wrongdelayline = []
        wrongfiles = []
        try:
            for files in range(numFilesLoaded):
                lengrange = min(len(self.datatb), len(dataframes[files]))
                identicalrow = 0
                differentrow = 0
                for rows in range(lengrange):
                    dataTBrow = self.datatb.loc[rows, :]
                    dataLVrow = dataframes[files].loc[rows, :]
                    delayTBrow = self.delaytb.values[rows][0]
                    delayLVrow = delayframes[files].values[rows][0]

                    if dataLVrow.equals(dataTBrow) and (delayLVrow in range(delayTBrow-self.toleranceValue,
                                                                            delayTBrow+self.toleranceValue+1)):
                        identicalrow += 1
                    else:
                        if not (delayLVrow in range(delayTBrow-self.toleranceValue, delayTBrow+self.toleranceValue+1)):
                            wrongdelayline.append(rows + 2)
                        if not dataLVrow.equals(dataTBrow):
                            wrongioline.append(rows + 2)
                        differentrow += 1
                if differentrow != 0:
                    differentfiles += 1
                    wrongfiles.append(nameframes[files])
                    resultmsg = reportfile((self.datatb.__len__()), (dataframes[files].__len__()), int(identicalrow),
                                           int(differentrow), wrongioline[:], wrongdelayline[:], nameframes[files], resultmsg)
                wrongioline = []
                wrongdelayline = []
                prog = ((files+1) / numFilesLoaded) * 100
                self.load_progress['value'] = prog
                self.load_progress.update()

            #Summary report and message of the full testing
            identicalfiles = numFilesLoaded - differentfiles
            successmsg = 'Identical files: ' + repr(identicalfiles) + '\nDifferent files: ' + repr(differentfiles)
            messagebox.showinfo("Results", successmsg)
            summaryfile(int(identicalfiles), int(differentfiles), wrongfiles[:], resultmsg)
            self.destroy()
        except NameError:
            messagebox.showinfo("Results", "Import the files first")
        except ValueError:
            messagebox.showinfo("Results", "Number of lines does not match.")

if __name__ == "__main__":
    root = tk.Tk()
    mainWindow = Verificationapp(root, "LGCS Verification Program", "300x300")
    root.mainloop()


