import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Initialize Database
DB_FILE = 'database.db'
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          email TEXT,
                          message TEXT)''')
        conn.commit()
init_db()

# Sample data for a business website
business_data = {
    "name": "Tech Solutions Inc.",
    "tagline": "Innovating the Future",
    "about": "We provide cutting-edge tech solutions to modern problems.",
    "services": [
        {"name": "Web Development", "description": "Building responsive and scalable web applications."},
        {"name": "AI Solutions", "description": "Implementing AI to optimize business processes."},
        {"name": "Cybersecurity", "description": "Protecting your digital assets from threats."}
    ],
    "team": [
        {"name": "John Doe", "role": "CEO"},
        {"name": "Jane Smith", "role": "CTO"},
        {"name": "Alice Brown", "role": "Lead Developer"}
    ],
    "testimonials": [
        {"author": "Client A", "text": "Tech Solutions Inc. transformed our business!"},
        {"author": "Client B", "text": "Outstanding support and innovation!"}
    ],
    "contact": {
        "email": "info@techsolutions.com",
        "phone": "+123 456 7890",
        "address": "123 Tech Street, Silicon Valley, CA"
    }
}

# Email Notification Function
def send_email(name, email, message):
    sender_email = "tom.jesica2024@gmail.com"
    receiver_email = "tom.jesica2024@gmail.com"
    subject = "New Contact Form Submission"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, "your-password")
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print("Error sending email:", e)

@app.route('/')
def home():
    return render_template('index.html', data=business_data)

@app.route('/about')
def about():
    return render_template('about.html', data=business_data)

@app.route('/services')
def services():
    return render_template('services.html', data=business_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
            conn.commit()
        send_email(name, email, message)
        return redirect('/contact-success')
    return render_template('contact.html', data=business_data)

@app.route('/contact-success')
def contact_success():
    return "Thank you! Your message has been received."

@app.route('/view-contacts')
def view_contacts():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, message FROM contacts")
        contacts = cursor.fetchall()
    return render_template('view_contacts.html', contacts=contacts)

# HTML Templates
html_templates = {
    "view_contacts.html": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact Submissions</title>
        <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'>
    </head>
    <body>
        <div class='container mt-4'>
            <h2>Contact Submissions</h2>
            <table class='table table-bordered'>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    {% for contact in contacts %}
                    <tr>
                        <td>{{ contact[0] }}</td>
                        <td>{{ contact[1] }}</td>
                        <td>{{ contact[2] }}</td>
                        <td>{{ contact[3] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
}

# Function to generate HTML templates
os.makedirs('templates', exist_ok=True)
for filename, content in html_templates.items():
    with open(f'templates/{filename}', 'w') as file:
        file.write(content)

if __name__ == '__main__':
    app.run(debug=True)
