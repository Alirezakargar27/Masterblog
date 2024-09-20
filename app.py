from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Define the path for the JSON file
JSON_FILE = os.path.join(os.getcwd(), "blog_posts.json")

def load_posts():
    """Loads the blog posts from the JSON file."""
    try:
        with open(JSON_FILE, "r") as fileobj:
            return json.load(fileobj)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file is not found or is empty, return an empty list
        return []

def save_blog_posts(posts):
    """Saves the updated list of blog posts to the JSON file."""
    with open(JSON_FILE, 'w') as fileobj:
        json.dump(posts, fileobj, indent=4)

def fetch_post_by_id(post_id):
    """Fetches a single blog post by its ID."""
    blog_posts = load_posts()
    return next((post for post in blog_posts if post['id'] == post_id), None)

@app.route('/hello')
def hello_world():
    return 'Hello, World! Here is Lais, your favourite coder!'

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing blog posts
        blog_posts = load_posts()

        # Create new blog post with a unique ID
        new_post = {
            'id': max(post['id'] for post in blog_posts) + 1 if blog_posts else 1,
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post and save the updated list
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)

        # Redirect to the home page to see the new post
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Handles deletion of a blog post."""
    # Load existing blog posts
    blog_posts = load_posts()

    # Filter out the post with the given id
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save updated list to the JSON file
    save_blog_posts(blog_posts)

    # Redirect back to the home page
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handles updating an existing blog post."""
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update post details
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Load all posts and update the specific post
        blog_posts = load_posts()
        for idx, p in enumerate(blog_posts):
            if p['id'] == post_id:
                blog_posts[idx] = post
                break

        # Save the updated list
        save_blog_posts(blog_posts)

        # Redirect to the index page
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)