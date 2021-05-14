from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.template_filter()
# Format DateTime: Thu 8 Apr 14:30:00 BST 2021
def datetimefilter(value, format='%a %d %b, %H:%M %z %Y'):
    return value.strftime(format)

# hooking to jinja env
app.jinja_env.filters['datetimefilter'] = datetimefilter


# create a UserAgentTracker model
class UserAgentTracker(db.Model):
    user_agent = db.Column(db.Text(), nullable=False, primary_key=True)
    visit_count = db.Column(db.Integer, nullable=False)
    last_visit_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Tracker {self.user_agent}"


@app.route('/', methods=['POST', 'GET'])
def index():
    # print(request.headers.get('User-Agent'))
    # get ALL agents
    trackers = UserAgentTracker.query.order_by(UserAgentTracker.last_visit_date).all()
    u_agent = request.headers.get('User-Agent')
    exists = UserAgentTracker.query.filter(UserAgentTracker.user_agent==u_agent).first()
    if exists is not None:
        # already in DB update count and Time
        # print("already added")
        exists.visit_count = int(exists.visit_count) + 1
        exists.last_visit_date = datetime.now()
        try:
            db.session.commit()
            return render_template('index.html', trackers=trackers)
        except:
            return "User Agents couldn't be updated!"
    else:
        # add to DB
        try:
            new_agent = UserAgentTracker(user_agent=u_agent, visit_count=1)
            db.session.add(new_agent)
            db.session.commit()
            # print("new user agent added")
            trackers = UserAgentTracker.query.order_by(UserAgentTracker.last_visit_date).all()
            return render_template('index.html', trackers=trackers)
        except:
            return 'There was an issue!'
    

if __name__ == "__main__":
    app.run(debug=True)