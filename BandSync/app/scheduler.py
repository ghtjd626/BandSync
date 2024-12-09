from ortools.sat.python import cp_model

class BandScheduler:
    def __init__(self):
        self.members = {}
        self.schedule = {}

    def add_member(self, name, availability, max_hours_per_week):
        """
        Add a band member and their availability.
        - name: Name of the member.
        - availability: List of available time slots (e.g., ['Monday-9AM', 'Tuesday-3PM']).
        - max_hours_per_week: Maximum practice hours per week.
        """
        self.members[name] = {
            'availability': availability,
            'max_hours': max_hours_per_week
        }

    def optimize_schedule(self, practice_duration):
        """
        Optimize a schedule that maximizes participation.
        - practice_duration: Duration of each session in hours.
        """
        model = cp_model.CpModel()

        # Define variables
        timeslots = set(slot for member in self.members.values() for slot in member['availability'])
        timeslot_vars = {
            (member, slot): model.NewBoolVar(f'{member}_{slot}')
            for member in self.members
            for slot in timeslots
        }

        # Constraint: Each member should not exceed their max hours per week.
        for member, data in self.members.items():
            model.Add(
                sum(timeslot_vars[member, slot] for slot in data['availability']) * practice_duration <= data['max_hours']
            )

        # Constraint: A single timeslot should not be overbooked.
        for slot in timeslots:
            model.Add(sum(timeslot_vars[member, slot] for member in self.members) <= 1)

        # Objective: Maximize participation
        model.Maximize(
            sum(timeslot_vars[member, slot] for member in self.members for slot in self.members[member]['availability'])
        )

        # Solve the model
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for member in self.members:
                self.schedule[member] = [
                    slot for slot in self.members[member]['availability']
                    if solver.BooleanValue(timeslot_vars[member, slot])
                ]
        else:
            print("No feasible solution found.")

    def print_schedule(self):
        """Display the generated schedule."""
        for member, slots in self.schedule.items():
            print(f"{member}: {', '.join(slots)}")

# Example usage
if __name__ == "__main__":
    scheduler = BandScheduler()
    scheduler.add_member("Alice", ["Monday-9AM", "Monday-10AM", "Tuesday-3PM"], max_hours_per_week=2)
    scheduler.add_member("Bob", ["Monday-9AM", "Tuesday-3PM", "Wednesday-4PM"], max_hours_per_week=3)
    scheduler.add_member("Charlie", ["Monday-9AM", "Monday-10AM", "Wednesday-4PM"], max_hours_per_week=1)

    scheduler.optimize_schedule(practice_duration=1)  # Each session lasts 1 hour
    scheduler.print_schedule()
