from flask import Flask, url_for, render_template, request, jsonify, redirect

from utils import posts, comments, bookmarks

app = Flask(__name__)
app.secret_key = "som_key"


@app.route("/")
def main():
    post_data = posts.get_posts_all()
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    return render_template("index.html", posts=post_data, bookmarks=bookmarks_activ)


@app.route("/posts/<int:post_id>")
def get_post_by_id(post_id):

    posts.add_view(post_id)
    post_data = posts.get_post_by_pk(post_id)
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    comments_data = comments.get_comments_by_post_id(post_id)

    return render_template('post.html', post=post_data, comments=comments_data, bookmarks=bookmarks_activ)


@app.route("/search/")
def search_data():
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    if request.args.get('Search'):
        search_string = request.args.get("Search")
        posts_data = posts.search_for_post(search_string)
        return render_template("search.html", posts=posts_data, search_string=search_string, bookmarks=bookmarks_activ)


@app.route('/user/<username>')
def get_user_posts(username):
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    posts_data = posts.get_posts_by_user(username)
    return render_template("user-feed.html", posts=posts_data, bookmarks=bookmarks_activ)


@app.route("/api/posts/")
def get_api_posts():
    posts_data = posts.get_posts_all()
    return jsonify(posts_data)


@app.route("/api/posts/<int:post_id>")
def get_api_post_by_id(post_id):
    post_data = posts.get_post_by_pk(post_id)
    # comments_data = comments.get_comments_by_post_id(post_id)
    return jsonify(post_data)


@app.route("/tag/<tagname>")
def get_posts_by_tags(tagname):
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    posts_data = posts.get_posts_by_tag(tagname)
    return render_template("tag.html", posts=posts_data, bookmarks=bookmarks_activ, tag=tagname)


@app.route('/bookmarks/')
def get_all_bookmarks():
    bookmarks_activ: list = bookmarks.get_bookmarks_activ()
    posts_data = posts.get_bookmarks_posts(bookmarks_activ)
    return render_template("bookmarks.html", posts=posts_data)


@app.route('/bookmarks/add/<int:postid>')
def add_bookmark(postid):
    bookmarks.add_bookmarks(postid)
    return redirect("/", code=302)


@app.route('/bookmarks/remove/<int:postid>')
def remove_bookmark(postid):
    bookmarks.remove_bookmarks(postid)
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run()
