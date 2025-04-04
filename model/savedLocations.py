from __init__ import app, db
import logging

class SavedLocation(db.Model):
    __tablename__ = 'saved_locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def create(self):
        """Create a new saved location entry in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error creating saved location: {str(e)}")
            return None
        return self

    def read(self):
        """Returns the saved location details as a dictionary."""
        return {
            "id": self.id,
            "name": self.name
        }

    def update(self, data):
        """Updates the saved location with new data and commits the changes."""
        if not self:
            raise ValueError("Saved location does not exist.")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error updating saved location: {str(e)}")
            raise e

    def delete(self):
        """Delete a saved location entry from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting saved location: {str(e)}")
            raise e

    @staticmethod
    def restore(data):
        """Restores saved locations from the provided data."""
        for location_data in data:
            _ = location_data.pop('id', None)
            name = location_data.get("name", None)
            location = SavedLocation.query.filter_by(name=name).first()
            if location:
                location.update(location_data)
            else:
                location = SavedLocation(**location_data)
                location.create()

def initSavedLocations():
    """Initialize the database with a few saved locations if none exist."""
    if not SavedLocation.query.first():
        saved_location_list = [
            SavedLocation(name="Home"),
            SavedLocation(name="Work"),
        ]

        for location in saved_location_list:
            location.create()
        print("Saved locations added to the database.")
    else:
        print("Saved locations already exist in the database.")
