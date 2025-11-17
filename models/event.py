class Event:
    def __init__(self, event_id, name, venue, start_date, end_date, start_time, final_entry_time, end_time):
        self.event_id = event_id
        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.final_entry_time = final_entry_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.name} at {self.venue} from {self.start_date} to {self.end_date}"