from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    # Redirect to another Flask app running on a specific IP and port
    return redirect(url_for('external_blog_app'))

@app.route('/about')
def about():
    return render_template('about.html')

# Define the external Flask app for the blog
external_blog_app = Flask(__name__)

@external_blog_app.route('/')
def external_blog_home():
    return "Welcome to the External Blog Home Page!"

@external_blog_app.route('/post/<int:post_id>')
def external_blog_post(post_id):
    return f"Viewing Blog Post #{post_id} on the External Blog App"

if __name__ == '__main__':
    # Run both Flask apps
    app.run(debug=True, port=5000)
    external_blog_app.run(host='127.0.0.1', port=5001)
