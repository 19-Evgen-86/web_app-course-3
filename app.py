from flask import Flask, render_template, request, jsonify, redirect

from utils import posts, comments, bookmarks, MyException

app = Flask(__name__)


@app.route("/")
def main():
    try:
        post_data = posts.get_posts_all()
        bookmarks_activ = bookmarks.get_bookmarks_activ()
        return render_template("index.html", posts=post_data, bookmarks=bookmarks_activ)
    except MyException:
        render_template("error.html")


@app.route("/posts/<int:post_id>")
def get_post_by_id(post_id):
    try:
        posts.add_view(post_id)
        post_data = posts.get_post_by_pk(post_id)
        bookmarks_activ = bookmarks.get_bookmarks_activ()
        comments_data = comments.get_comments_by_post_id(post_id)
        return render_template('post.html', post=post_data, comments=comments_data, bookmarks=bookmarks_activ)
    except MyException:
        render_template("error.html")


@app.route("/search/")
def search_data():
    try:
        bookmarks_activ = bookmarks.get_bookmarks_activ()
        if request.args.get('Search'):
            search_string = request.args.get("Search")
            posts_data = posts.search_for_post(search_string)
            return render_template("search.html", posts=posts_data, search_string=search_string,
                                   bookmarks=bookmarks_activ)
    except MyException:
        render_template("error.html")


@app.route('/user/<username>')
def get_user_posts(username):
    try:
        bookmarks_activ = bookmarks.get_bookmarks_activ()
        posts_data = posts.get_posts_by_user(username)
        if posts_data:
            return render_template("user-feed.html", posts=posts_data, bookmarks=bookmarks_activ)
        else:
            return render_template("notresultsearch.html")
    except MyException:
        render_template("error.html")


@app.route("/api/posts/")
def get_api_posts():
    try:
        posts_data = posts.get_posts_all()
        return jsonify(posts_data)
    except MyException:
        render_template("error.html")


@app.route("/api/posts/<int:post_id>")
def get_api_post_by_id(post_id):
    try:
        post_data = posts.get_post_by_pk(post_id)
        # comments_data = comments.get_comments_by_post_id(post_id)
        return jsonify(post_data)
    except MyException:
        render_template("error.html")


@app.route("/tag/<tagname>")
def get_posts_by_tags(tagname):
    try:
        bookmarks_activ = bookmarks.get_bookmarks_activ()
        posts_data = posts.get_posts_by_tag(tagname)
        return render_template("tag.html", posts=posts_data, bookmarks=bookmarks_activ, tag=tagname)
    except MyException:
        render_template("error.html")


@app.route('/bookmarks/')
def get_all_bookmarks():
    try:
        bookmarks_activ: list = bookmarks.get_bookmarks_activ()
        posts_data = posts.get_bookmarks_posts(bookmarks_activ)
        if posts_data:
            return render_template("bookmarks.html", posts=posts_data)
        else:
            return render_template('notresultsearch.html')
    except MyException:
        render_template("error.html")


@app.route('/bookmarks/add/<int:postid>')
def add_bookmark(postid):
    try:
        bookmarks.add_bookmarks(postid)
        return redirect("/", code=302)
    except MyException:
        render_template("error.html")


@app.route('/bookmarks/remove/<int:postid>')
def remove_bookmark(postid):
    try:
        bookmarks.remove_bookmarks(postid)
        return redirect("/", code=302)
    except MyException:
        render_template("error.html")


if __name__ == '__main__':
    app.run()
