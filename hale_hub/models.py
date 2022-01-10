from hale_hub.extensions import db
from hale_hub.constants import MAX_STRING_LENGTH


class RoomStatModel(db.Model):
    """Table containing statistics on rooms around house. Different variables should be grouped together around
    the same lock-stepped time frame"""

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)
    variable_name = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)
    units = db.Column(db.String(MAX_STRING_LENGTH), nullable=True)
    value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)

    def __repr__(self):
        return '<Date %r, Location %r, Variable %r, Value %f, Units %r, Status %r>' % (self.date, self.location, self.variable_name,
                                                                                       self.value, self.units, self.status)


class UserFeedbackModel(db.Model):
    """Table containing user feedback."""

    id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)
    user = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)
    variable_name = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<User %r, Feedback %r, Value %r>' % (self.user, self.variable_name, self.value)
