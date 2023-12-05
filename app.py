# Flask application (app.py)

from flask import Flask, request, render_template
import win32com.client as win32
import pythoncom

app = Flask(__name__)

def send_status_email(subject, recipients, last_week_tasks, this_week_tasks, sender_name):
    pythoncom.CoInitialize()

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.To = recipients
    
    # Use HTML body for rich text formatting
    body = f"""
    <html>
        <body>
            <p><strong>Last Week's Tasks:</strong></p>
            {last_week_tasks}
            <p><strong>This Week's Tasks:</strong></p>
            {this_week_tasks}
            <p>Best regards,<br>
            {sender_name}</p>
        </body>
    </html>
    """
    
    mail.HTMLBody = body
    mail.Send()
    
    pythoncom.CoUninitialize()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_status_email', methods=['POST'])
def send_status_email_route():
    subject = request.form['subject']
    recipients = request.form['recipients']
    sender_name = request.form['sender_name']
    # Get the HTML content for tasks
    last_week_tasks = request.form['last_week_tasks']
    this_week_tasks = request.form['this_week_tasks']

    send_status_email(subject, recipients, last_week_tasks, this_week_tasks, sender_name)
    return 'Status email sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
