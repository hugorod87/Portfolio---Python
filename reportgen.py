
import webbrowser
import datetime
from itertools import groupby, count


# This is to seperate the wrong lines into ranges
def intervals(data):
    out = []
    counter = count()

    for key, group in groupby(data, key=lambda x: x - next(counter)):
        block = list(group)
        out.append([block[0], block[-1]])
    return out


def reportfile(tblines, lvlines, numcorrect, numwrong, linewrong, delaywrong, docid, oldvalue):
    linewrong = intervals(linewrong)
    delaywrong = intervals(delaywrong)
    message = """<html>
    <body><p><h3><div id="%s">%s</div></h3>
    Number of lines in the Testbench results: <b>%i</b> <br>
    Number of lines in the LabView results: <b>%i</b> <br>
    Number of lines that matched: <b>%i</b> <br>
    Number of lines that mismatched: <b>%i</b> <br>
    Range of lines that has different Input/Output from the simulation results: <b>%s</b> <br>
    Range of lines that has different Delay Between States from the simulation results: <b>%s</b> <br><br>
    </p></body>
    </html>"""
    indfiles = message % (docid, docid, tblines, lvlines, numcorrect, numwrong, linewrong, delaywrong)
    return (oldvalue + indfiles)


def summaryfile(filesidentical, filedifferent, wrongfiles, wrongdoc):
    global listoffiles
    now = datetime.datetime.today().strftime("%Y/%m/%d - %H:%M:%S")
    with open("Summary.html", "w") as myFile:
        htmlresults = """<html>
    <p><h1>Verification & Validation File  --  Generated at: %s </h1><br><h2>Project 8 - LGCS Test Results<br>
    Report Summary:</h2><br>
    <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Type of Files', 'Number'],
          ['Approved', %i],
          ['Disapproved', %i]
        ]);

        var options = {
          title: 'Files Verified:'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="piechart" style="width: 400px; height: 200px;"></div>
    Number of Identical Files: <b>%i</b> <br><br>
    Number of Different Files: <b>%i</b> <br><br>
    Files that are different from the simulation: """
        resultstext1 = htmlresults % (now, filesidentical, filedifferent, filesidentical, filedifferent)
        myFile.write(resultstext1)
        for i in range(filedifferent):
            listoffiles = """<a href="#%s">%s, </a>"""
            resultstext2 = listoffiles % (wrongfiles[i], wrongfiles[i])
            myFile.write(resultstext2)
        descriptions = """<br><br>Here is the description of all the files that was <b>NOT</b> validated: <br>
        %s </p></body></html>"""
        resultstext3 = descriptions % (wrongdoc)
        myFile.write(resultstext3)
    webbrowser.open_new_tab("Summary.html")
