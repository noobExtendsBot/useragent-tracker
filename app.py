from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'M\rn\xe2q\xf3\xc6\xf6\x05\xe7K\xb1\x83j\xba1n\x85b\xca\t\xc6\x9f='
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.template_filter()
# Format DateTime: Thu 8 Apr 14:30:00 BST 2021
def datetimefilter(value, format='%a %d %b, %H:%M %z %Y'):
    return value.strftime(format)

# hooking to jinja env
app.jinja_env.filters['datetimefilter'] = datetimefilter


class Tracker():
    user_agent_dict = dict()
    l = 0
    def __init__(self):
        """
            expected data format
            {
                "user_agent": [1, 'date'],
                "user_agent2": [2, 'date'],
            }
        """
        self.l = len(self.user_agent_dict)
        # print("new Tracker obj created")
        
    def add_new(self, user_agent):
        self.user_agent_dict[user_agent] = [1, str(datetime.now())]
        self.l = self.l + 1
        print(self.user_agent_dict)
        return True

    # TO UPDATE THE VISIT_COUNT
    def update_count(self, user_agent):
        # print(self.l)
        if self.l >= 0:
            self.user_agent_dict[user_agent][0] = int(self.user_agent_dict[user_agent][0]) + 1
            return True
    
    def update_last_visit_date(self, user_agent):
        self.user_agent_dict[user_agent][1] = str(datetime.now())
        return True

@app.route('/', methods=['POST', 'GET'])
def index():
    trackers = ()
    u_agent = request.headers.get('User-Agent')
    if 'tracker_data' in session:
        session.pop('tracker_data', None)

    if tracker.l == 0:
        tracker.add_new(u_agent)
        # tracker.update_count(u_agent)
        trackers = str(tracker.user_agent_dict)
        tracker.update_last_visit_date(u_agent)
        return render_template('index.html', trackers=eval(trackers))
    elif tracker.l > 0:
        try:
            tracker.user_agent_dict[u_agent]
            tracker.update_count(u_agent)
            trackers = str(tracker.user_agent_dict)
            tracker.update_last_visit_date(u_agent)
            return render_template('index.html', trackers=eval(trackers))
        except KeyError:
            tracker.add_new(u_agent)
            # tracker.update_count(user_agent)
            trackers = str(tracker.user_agent_dict)
            tracker.update_last_visit_date(u_agent)
            return render_template('index.html', trackers=eval(trackers))    

if __name__ == "__main__":
    tracker = Tracker()
    app.run(debug=True)