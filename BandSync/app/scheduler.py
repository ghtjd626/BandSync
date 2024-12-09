import pandas as pd
from datetime import datetime, timedelta
from itertools import product

class BandScheduler:
    def __init__(self):
        self.members = pd.DataFrame()

    def add_member(self, name, location, availability):
        """
        Add a band member with their location and weekly availability.
        :param name: Member's name
        :param location: Member's location (e.g., NY, LA)
        :param availability: A list of available time slots (e.g., ["Mon 10:00-12:00", "Wed 14:00-16:00"])
        """
        self.members = pd.concat([self.members, pd.DataFrame([{
            'name': name,
            'location': location,
            'availability': availability
        }])], ignore_index=True)

    def find_schedule(self, location=None):
        """
        Suggest an optimal schedule for a band practice.
        :param location: Optional location filter for scheduling.
        :return: Suggested schedule with maximum attendance.
        """
        # Filter members by location if specified
        members = self.members
        if location:
            members = members[members['location'] == location]

        # Collect all availability slots
        all_slots = []
        for _, member in members.iterrows():
            for slot in member['availability']:
                day, times = slot.split()
                start, end = times.split('-')
                all_slots.append({
                    'name': member['name'],
                    'day': day,
                    'start': datetime.strptime(start, "%H:%M"),
                    'end': datetime.strptime(end, "%H:%M")
                })

        # Generate potential time slots
        time_slots = self._generate_time_slots(all_slots)

        # Evaluate attendance for each time slot
        attendance = self._evaluate_attendance(time_slots, all_slots)

        # Return the best time slot(s)
        return sorted(attendance, key=lambda x: -x['attendees'])

    def _generate_time_slots(self, all_slots):
        """
        Generate possible time slots from the given availability.
        """
        days = set(slot['day'] for slot in all_slots)
        times = [datetime.strptime("08:00", "%H:%M") + timedelta(minutes=30 * i) for i in range(20)]
        return [{'day': day, 'start': t, 'end': t + timedelta(hours=1)} for day, t in product(days, times)]

    def _evaluate_attendance(self, time_slots, all_slots):
        """
        Evaluate how many members can attend each time slot.
        """
        results = []
        for slot in time_slots:
            attendees = 0
            for member_slot in all_slots:
                if member_slot['day'] == slot['day'] and \
                   member_slot['start'] <= slot['start'] and \
                   member_slot['end'] >= slot['end']:
                    attendees += 1
            results.append({**slot, 'attendees': attendees})
        return results

# Example usage
if __name__ == "__main__":
    scheduler = BandScheduler()
    scheduler.add_member("Alice", "NY", ["Mon 10:00-12:00", "Wed 14:00-16:00"])
    scheduler.add_member("Bob", "NY", ["Mon 11:00-13:00", "Wed 15:00-17:00"])
    scheduler.add_member("Charlie", "NY", ["Mon 10:30-12:30", "Wed 14:00-16:30"])

    suggested_schedule = scheduler.find_schedule(location="NY")
    for slot in suggested_schedule[:5]:  # Show top 5 slots
        print(f"Day: {slot['day']}, Start: {slot['start'].strftime('%H:%M')}, End: {slot['end'].strftime('%H:%M')}, Attendees: {slot['attendees']}")
