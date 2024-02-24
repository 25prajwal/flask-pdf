from flask import Flask, jsonify , request, send_file
import PyPDF2
import os

app = Flask(__name__)


@app.route('/')
def index():
    return ("Hello World! v2 <br> Dev : Prajwal Kedari <br> <a href="/Cheatpdf">Use App</a>)
@app.route('/Cheatpdf_work', methods = ['POST'])
def split_pdf():
   if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        pdf_file = open(f.filename, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_output = PyPDF2.PdfWriter()
        k=0
        s=9 #No. of page per Page
        nPage=len(pdf_reader.pages ) #no. of page
        for i in range(s*2,(int(nPage/18)*18)+1,s*2):
            for j in range(k,i,2):
                print("==========>",j)
                pdf_output.add_page(pdf_reader.pages[j])
            for j in range(k+1,i+1,2):
                pdf_output.add_page(pdf_reader.pages[j])
                print("------------------------------>",j)
            k=i
        oPage=int(nPage%18)
        if oPage:
            for i in range(0,(oPage),2):
                print("==========>------------",i+k)
                pdf_output.add_page(pdf_reader.pages[i+k])
            for i in range(10-round(oPage/2)):
                pdf_output.add_blank_page()
            for i in range(1,(oPage),2):
                pdf_output.add_page(pdf_reader.pages[i+k])

        with open(f.filename,"wb") as (out):
            pdf_output.write(out)
        return send_file(f.filename,mimetype='application/pdf')
   return "no file"

@app.route('/Cheatpdf')
def pdfGet():
    html='''<form action = "/Cheatpdf_work" method = "post" enctype="multipart/form-data">
        <input type="file" name="file" />
        <input type = "submit" value="Upload">
    </form>
    '''
    return html

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
