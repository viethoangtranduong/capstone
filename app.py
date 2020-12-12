from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route('/')
def student():
   method = "The summarization method will be here"
   summary = "Your summary output"
   length = "Length of the summary"
   return render_template('student.html', method = method, summary = summary, length = length)

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      url = request.form['url_for_news']
      text = request.form['text_for_news']
      num_sentence = request.form['num_sentence']
      # print("checkpoint0")
      if url:
         BASE1 = 'http://ec2-18-232-83-67.compute-1.amazonaws.com:3000/'
         json_req = {"News_url": url}
         response = requests.put(BASE1 + "running", json_req)
         response = response.json()
         # print("checkpoint1", response)
         if "text" in response and response["text"] != "Error":
            text = response["text"]
      # print("pass 1. text:", text)
      if text:
         BASE2 = 'http://ec2-54-221-124-167.compute-1.amazonaws.com:3001/'
         if num_sentence:
            json_req = {"text_in": text, "len_out": int(num_sentence)}
         else:
            json_req = {"text_in": text}

         response = requests.put(BASE2 + "running", json_req)
         response = response.json()
         # print("checkpoint2", response)
         summary = response["text_out"]
         length = response['len_out']
         method = response["method"]

      else:
         method = "Need either valid text or url"
         summary = ""
         length = 0
      # print("pass 1. summary:", summary)

      return render_template("student.html", method = method, summary = summary, length = length)

if __name__ == '__main__':
   app.run(debug = True)
