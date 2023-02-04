from tkinter import *
import pandas as pd
from tkcalendar import Calendar
import os

ws = Tk()

ws.title("Attendance Management System")
ws.geometry("1080x1080")
ws['bg'] = '#012'

Alignx = 300
Aligny = 270
rows = 0

database = pd.read_csv('student_attendance_database.csv')
database.head()
if os.path.isfile('Attendance Report.csv'):
    Attendance = pd.read_csv('Attendance Report.csv')
else:
    Attendance = pd.DataFrame(columns=['Name', 'Roll_number', 'section', 'date', 'subject', 'status'])
subjects = ['Maths', 'Physics', 'Chemistry']


class AttendanceSheet:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Name', 'Roll_number', 'section', 'date', 'subject', 'status'])

    def existing_sheet(self, section, date, subject):
        data = database[database['section'] == section]
        data['date'] = [date for i in range(len(data))]
        data['subject'] = [subject for i in range(len(data))]
        data['status'] = ['absent' for i in range(len(data))]
        self.data = data

    def new_sheet(self, names, rollnumbers, section, date, subject):
        data = pd.DataFrame()
        data['Name'] = names
        data['Roll_number'] = rollnumbers
        data['section'] = [section for i in range(len(data))]
        data['date'] = [date for i in range(len(data))]
        data['subject'] = [subject for i in range(len(data))]
        data['status'] = ['absent' for i in range(len(data))]
        self.data = data

    def mark_attendance(self, rollnumber):
        self.data.loc[self.data['Roll_number'] == rollnumber, 'status'] = 'present'

    def mark_attendance_ab(self, rollnumber):
        self.data.loc[self.data['Roll_number'] == rollnumber, 'status'] = 'absent'

    def update(self):
        global Attendance
        Attendance = pd.concat([Attendance, self.data])
        self.data = pd.DataFrame(columns=['Name', 'Roll_number', 'section', 'date', 'subject', 'status'])


class Display:
    def __init__(self, name=None, roll=None, section=None, date=None, subject=None, status=None):
        self.name = name
        self.roll = roll
        self.section = section
        self.date = date
        self.subject = subject
        self.status = status
        self.data = pd.DataFrame(columns=['Name', 'Roll_number', 'section', 'date', 'subject', 'status'])

    def process(self):
        global Attendance
        attr = {'Name': self.name, 'Roll_number': self.roll, 'section': self.section, 'date': self.date,
                'subject': self.subject, 'status': self.status}
        df = pd.DataFrame(columns=['Name', 'Roll_number', 'section', 'date', 'subject', 'status'])
        for i in attr.keys():
            if attr[i]:
                if len(df) == 0:
                    df = Attendance[attr[i] == Attendance[i]]
                else:
                    df = df[df[i] == attr[i]]
        self.data = df
        return df


def studentsheet():
    cs = Tk()
    cs.title("Attendance Management System")
    cs.geometry("1080x1080")
    cs['bg'] = '#012'
    select_section = StringVar(cs)
    select_section.set("Select an Option")
    select_subject = StringVar(cs)
    select_subject.set("Select an Option")

    def createsheet():
        x = AttendanceSheet()
        x.existing_sheet(select_section.get(), select_date.get_date(), select_subject.get())
        cs.destroy()
        ds = Tk()
        ds.title("Attendance Management System")
        ds.geometry("1080x1080")
        ds['bg'] = '#012'
        report = {x.data.iloc[i, 1]: IntVar(ds) for i in range(len(x.data))}
        total_rows = len(x.data)
        total_columns = len(x.data.columns)

        def display_sheet():
            global rows
            for j in range(total_columns):
                if j == 0:
                    e = Entry(ds, width=50, fg='blue',
                              font=('Arial', 12, 'bold'))
                    e.grid(row=0, column=j)
                    e.insert(END, x.data.columns[j])
                else:
                    e = Entry(ds, width=10, fg='blue',
                              font=('Arial', 12, 'bold'))
                    e.grid(row=0, column=j)
                    e.insert(END, x.data.columns[j])
            for i in range(rows, min(rows + 25, total_rows)):
                for j in range(total_columns):
                    if j == 0:
                        e = Entry(ds, width=50, fg='blue',
                                  font=('Arial', 12, 'bold'))
                        e.grid(row=i + 1 - rows, column=j)
                        e.insert(END, x.data.iloc[i, j])
                    elif j == total_columns - 1:
                        Checkbutton(ds, text="", variable=report[x.data.iloc[i, 1]], onvalue=1, offvalue=0, height=1,
                                    width=10).grid(row=i + 1 - rows, column=j)

                    else:
                        e = Entry(ds, width=10, fg='blue',
                                  font=('Arial', 12, 'bold'))
                        e.grid(row=i + 1 - rows, column=j)
                        e.insert(END, x.data.iloc[i, j])

            def inc():
                global rows
                rows = min(rows + 25, total_rows)

                display_sheet()

            def dec():
                global rows
                rows = max(rows - 25, 0)
                display_sheet()

            Button(ds, text="prev", font='Arial 16', command=dec, width=3, height=1).place(x=Alignx + 630,
                                                                                           y=Aligny + 400)
            Button(ds, text="next", font='Arial 16', command=inc, width=3, height=1).place(x=Alignx + 700,
                                                                                           y=Aligny + 400)

        def finalizerep():
            for i in report:
                if report[i].get():
                    x.mark_attendance(i)
                else:
                    x.mark_attendance_ab(i)
            x.update()
            rows = 0
            ds.destroy()

        Button(ds, text="Submit", font='Arial 16', command=finalizerep, width=10, height=1).place(x=Alignx + 630,
                                                                                                  y=Aligny + 200)

        display_sheet()
        ds.mainloop()

    Label(cs, text="Select Options", fg="#ffffff",bg="#012",font='Arial 32', width=20, height=1).place(
        x=Alignx , y=Aligny-100 )
    Label(cs, text="Date", font='Arial 16', width=20, height=1).place(
        x=Alignx-100, y=Aligny+20)
    select_date = Calendar(cs, selectmode='day',date_pattern="dd/mm/yyyy")
    select_date.place(x=Alignx - 100, y=Aligny + 50)
    Label(cs, text="Section", font='Arial 16', width=10, height=1).place(
        x=Alignx +200, y=Aligny + 20)
    OptionMenu(cs, select_section, *sorted(list(database['section'].unique()))).place(x=Alignx + 200, y=Aligny + 50)
    Label(cs, text="Subject", font='Arial 16', width=10, height=1).place(
        x=Alignx + 350, y=Aligny + 20)
    OptionMenu(cs, select_subject, *subjects).place(x=Alignx + 350, y=Aligny + 50)

    Button(cs, text="Get Sheet", font='Arial 16', command=createsheet, width=10, height=1).place(x=Alignx + 350,
                                                                                                 y=Aligny + 200)
    cs.mainloop()


def Query_sheet():
    qs = Tk()
    qs.title("Attendance Management System")
    qs.geometry("1080x1080")
    qs['bg'] = '#012'
    name = StringVar(qs)
    roll = StringVar(qs)
    sec = StringVar(qs)
    sec.set("Select the options")
    sub = StringVar(qs)
    sub.set("Select the options")
    sts = StringVar(qs)
    sts.set("None")
    Label(qs, text="Name :", font=('Arial', 16),fg='#ffffff',bg='#012', width=12).place(x=Alignx, y=Aligny - 200)
    Entry(qs, width=25, font='Arial 16', textvariable=name).place(x=Alignx + 180, y=Aligny - 200)
    Label(qs, text="Roll No. :", font=('Arial', 16),fg='#ffffff',bg='#012', width=12).place(x=Alignx, y=Aligny - 140)
    Entry(qs, width=25, font='Arial 16', textvariable=roll).place(x=Alignx + 180, y=Aligny - 140)
    Label(qs, text="Section :", font=('Arial', 16),fg='#ffffff',bg='#012', width=12).place(x=Alignx, y=Aligny - 80)
    OptionMenu(qs, sec, *sorted(list(database['section'].unique()))).place(x=Alignx + 180, y=Aligny - 80)
    Label(qs, text="Date :", font=('Arial', 16),fg='#ffffff',bg='#012', width=12).place(x=Alignx, y=Aligny)
    date = Calendar(qs,selectmode='day',date_pattern="dd/mm/yyyy")
    date.place(x=Alignx + 180, y=Aligny)
    Label(qs, text="Subject :", font=('Arial', 16),fg='#ffffff',bg='#012', width=12).place(x=Alignx, y=Aligny + 190)
    OptionMenu(qs, sub, *subjects).place(x=Alignx + 180, y=Aligny + 190)
    Label(qs, text="Status :", font=('Arial', 16),fg='#ffffff',bg='#012', width=12).place(x=Alignx, y=Aligny + 250)
    OptionMenu(qs, sts, *['present','absent']).place(x=Alignx + 180, y=Aligny + 250)
    # Entry(qs, width=25, font='Arial 16', textvariable=sts).place(x=Alignx + 180, y=Aligny + 250)

    def run():
        nm = name.get()
        nm = nm.upper() if nm else None
        rn = roll.get()
        rn = rn.replace('s', 'S') if rn else None
        sn = sec.get()
        sn = sn[:2].upper()
        dt = date.get_date()
        for i in set(Attendance['date']):
            if i == dt:
                break
        else:
            dt = None
        sb = sub.get().capitalize()
        sb = sb if sb in subjects else None
        st = sts.get().lower()
        st = st if st in ['absent', 'present'] else None
        x = Display(name=nm, roll=rn, date=dt, section=sn, subject=sb, status=st)
        report = x.process()
        qs.destroy()
        qd = Tk()
        qd.title("Attendance Management System")
        qd.geometry("1080x1080")
        qd['bg'] = '#012'
        total_rows = len(report)
        total_columns = len(report.columns)

        def display_sheet():
            global rows
            for j in range(total_columns):
                if j == 0:
                    e = Entry(qd, width=50, fg='blue',
                              font=('Arial', 12, 'bold'))
                    e.grid(row=0, column=j)
                    e.insert(END, report.columns[j])
                else:
                    e = Entry(qd, width=10, fg='blue',
                              font=('Arial', 12, 'bold'))
                    e.grid(row=0, column=j)
                    e.insert(END, report.columns[j])
            for i in range(rows, min(rows + 25, total_rows)):
                for j in range(total_columns):
                    if j == 0:
                        e = Entry(qd, width=50, fg='blue',
                                  font=('Arial', 12, 'bold'))
                        e.grid(row=i + 1 - rows, column=j)
                        e.insert(END, report.iloc[i, j])
                    else:
                        e = Entry(qd, width=10, fg='blue',
                                  font=('Arial', 12, 'bold'))
                        e.grid(row=i + 1 - rows, column=j)
                        e.insert(END, report.iloc[i, j])

            def inc():
                global rows
                rows = min(rows + 25, total_rows)
                display_sheet()

            def dec():
                global rows
                rows = max(rows - 25, 0)
                display_sheet()

            Button(qd, text="prev", font='Arial 16', command=dec, width=3, height=1).place(x=Alignx + 630,
                                                                                           y=Aligny + 400)
            Button(qd, text="next", font='Arial 16', command=inc, width=3, height=1).place(x=Alignx + 700,
                                                                                           y=Aligny + 400)

        display_sheet()
        qd.mainloop()

    Button(qs, text="Submit", font='Arial 16', command=run, width=10, height=1).place(x=Alignx + 90, y=Aligny + 300)
    qs.mainloop()


def save_file():
    Attendance.to_csv(f"Attendance Report.csv", index=False)
    ws.destroy()


Label(ws, text="Attendance Management System",font='Arial 25',fg='#ffffff',bg='#012',width=30, height=1).place(x=Alignx, y=Aligny-100)

Button(ws, text="Mark Attendance", font='Arial 16', command=studentsheet, width=20, height=2).place(x=Alignx, y=Aligny)
Button(ws, text="Display Attendance", font='Arial 16', command=Query_sheet, width=20, height=2).place(x=Alignx + 300,
                                                                                                      y=Aligny)
Button(ws, text="Update & Exit", font='Arial 16', command=save_file, width=20, height=1).place(x=Alignx+150, y=Aligny + 120)
ws.mainloop()
