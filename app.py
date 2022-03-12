from flask import Flask, render_template, request, jsonify, redirect

from utils import posts, comments, bookmarks, MyException, catch_error

app = Flask(__name__)


@app.route("/")
@catch_error
def main():
    post_data = posts.get_posts_all()
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    return render_template("index.html", posts=post_data, bookmarks=bookmarks_activ)


@app.route("/posts/<int:post_id>")
@catch_error
def get_post_by_id(post_id):
    posts.add_view(post_id)
    post_data = posts.get_post_by_pk(post_id)
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    comments_data = comments.get_comments_by_post_id(post_id)
    return render_template('post.html', post=post_data, comments=comments_data, bookmarks=bookmarks_activ)


@app.route("/search/")
@catch_error
def search_data():
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    if request.args.get('Search'):
        search_string = request.args.get("Search")
        posts_data = posts.search_for_post(search_string)
        return render_template("search.html", posts=posts_data, search_string=search_string,
                               bookmarks=bookmarks_activ)


@app.route('/user/<username>')
@catch_error
def get_user_posts(username):
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    posts_data = posts.get_posts_by_user(username)
    if posts_data:
        return render_template("user-feed.html", posts=posts_data, bookmarks=bookmarks_activ)
    else:
        return render_template("notresultsearch.html")


@app.route("/api/posts/")
@catch_error
def get_api_posts():
    posts_data = posts.get_posts_all()
    return jsonify(posts_data)


@app.route("/api/posts/<int:post_id>")
@catch_error
def get_api_post_by_id(post_id):
    post_data = posts.get_post_by_pk(post_id)
    # comments_data = comments.get_comments_by_post_id(post_id)
    return jsonify(post_data)


@app.route("/tag/<tagname>")
@catch_error
def get_posts_by_tags(tagname):
    bookmarks_activ = bookmarks.get_bookmarks_activ()
    posts_data = posts.get_posts_by_tag(tagname)
    return render_template("tag.html", posts=posts_data, bookmarks=bookmarks_activ, tag=tagname)


@app.route('/bookmarks/')
@catch_error
def get_all_bookmarks():
    bookmarks_activ: list = bookmarks.get_bookmarks_activ()
    posts_data = posts.get_bookmarks_posts(bookmarks_activ)
    if posts_data:
        return render_template("bookmarks.html", posts=posts_data)
    else:
        return render_template('notresultsearch.html')


@app.route('/bookmarks/add/<int:postid>')
@catch_error
def add_bookmark(postid):
    bookmarks.add_bookmarks(postid)
    return redirect("/", code=302)


@app.route('/bookmarks/remove/<int:postid>')
@catch_error
def remove_bookmark(postid):
    bookmarks.remove_bookmarks(postid)
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run()
